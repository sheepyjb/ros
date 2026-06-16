# YOLO Backend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a real Ultralytics YOLO backend to `robot_perception` while keeping the existing color detector as a fallback.

**Architecture:** Keep one ROS node, `image_detector_node`, and select the detection backend with `detector_backend:=color|yolo`. Put YOLO-specific model loading and result conversion in `robot_perception/yolo_detector.py` so ROS message publication and debug-image publication stay in the existing node.

**Tech Stack:** ROS 2 Jazzy, `rclpy`, `cv_bridge`, OpenCV, Ultralytics YOLO, Python `unittest`, `colcon`.

---

## File Structure

- Create: `src/robot_perception/robot_perception/yolo_detector.py`
  - Loads Ultralytics lazily.
  - Converts one YOLO result to `DetectionResult`.
  - Selects the highest-confidence accepted object.
- Create: `src/robot_perception/test/test_yolo_detector.py`
  - Uses fake YOLO model/results, so tests do not need `ultralytics`.
- Modify: `src/robot_perception/robot_perception/image_detector_node.py`
  - Declares `detector_backend`, `yolo_model_path`, `yolo_confidence_threshold`, and `yolo_target_class`.
  - Calls color or YOLO backend from `image_callback`.
- Create: `src/robot_perception/config/yolo_detector.yaml`
  - Default YOLO parameters.
- Create: `src/robot_perception/launch/yolo_detector.launch.py`
  - Starts the same node in YOLO mode.
- Modify: `src/robot_perception/test/test_perception_assets.py`
  - Covers new assets and node parameters.
- Create: `src/robot_perception/WEEK_05_02_YOLO_BACKEND.md`
  - Course handout for installing YOLO in WSL and running the backend.
- Modify: `src/robot_perception/README.md`, `README.md`, `ros2_learning_notes.md`
  - Add the new lesson entry and commands.
- Modify: `CODEX_CONTEXT.md`
  - Append the final progress snapshot after verification.

## Task 1: YOLO Adapter

**Files:**
- Create: `src/robot_perception/test/test_yolo_detector.py`
- Create: `src/robot_perception/robot_perception/yolo_detector.py`

- [ ] **Step 1: Write the failing adapter tests**

Create `src/robot_perception/test/test_yolo_detector.py`:

```python
import unittest

import numpy as np

from robot_perception.yolo_detector import YoloObjectDetector, detection_from_yolo_result


class FakeBoxes:
    def __init__(self, xyxy, conf, cls):
        self.xyxy = xyxy
        self.conf = conf
        self.cls = cls


class FakeResult:
    def __init__(self, xyxy, conf, cls, names):
        self.boxes = FakeBoxes(xyxy, conf, cls)
        self.names = names


class FakeModel:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def __call__(self, image, verbose=False):
        self.calls.append((image, verbose))
        return [self.result]


class YoloDetectorTest(unittest.TestCase):
    def test_converts_highest_confidence_box_to_normalized_detection(self):
        result = FakeResult(
            xyxy=[[10.0, 20.0, 50.0, 80.0], [100.0, 10.0, 180.0, 50.0]],
            conf=[0.40, 0.90],
            cls=[0.0, 1.0],
            names={0: "person", 1: "sports ball"},
        )

        detection = detection_from_yolo_result(
            result,
            image_shape=(100, 200, 3),
            confidence_threshold=0.25,
            target_class="",
        )

        self.assertTrue(detection.is_tracking)
        self.assertEqual("sports ball", detection.label)
        self.assertAlmostEqual(0.90, detection.confidence)
        self.assertAlmostEqual(0.70, detection.center_x, places=2)
        self.assertAlmostEqual(0.30, detection.center_y, places=2)
        self.assertAlmostEqual(0.40, detection.width, places=2)
        self.assertAlmostEqual(0.40, detection.height, places=2)

    def test_ignores_boxes_below_confidence_threshold(self):
        result = FakeResult(
            xyxy=[[10.0, 20.0, 50.0, 80.0]],
            conf=[0.20],
            cls=[0.0],
            names={0: "person"},
        )

        detection = detection_from_yolo_result(
            result,
            image_shape=(100, 200, 3),
            confidence_threshold=0.25,
            target_class="",
        )

        self.assertFalse(detection.is_tracking)
        self.assertEqual("", detection.label)

    def test_filters_by_target_class_name(self):
        result = FakeResult(
            xyxy=[[10.0, 20.0, 50.0, 80.0], [100.0, 10.0, 180.0, 50.0]],
            conf=[0.95, 0.90],
            cls=[0.0, 1.0],
            names={0: "person", 1: "sports ball"},
        )

        detection = detection_from_yolo_result(
            result,
            image_shape=(100, 200, 3),
            confidence_threshold=0.25,
            target_class="sports ball",
        )

        self.assertTrue(detection.is_tracking)
        self.assertEqual("sports ball", detection.label)
        self.assertAlmostEqual(0.90, detection.confidence)

    def test_detector_calls_injected_model_without_requiring_ultralytics(self):
        image = np.zeros((100, 200, 3), dtype=np.uint8)
        result = FakeResult(
            xyxy=[[10.0, 20.0, 50.0, 80.0]],
            conf=[0.80],
            cls=[0.0],
            names={0: "person"},
        )
        model = FakeModel(result)
        detector = YoloObjectDetector(
            model_path="unused.pt",
            confidence_threshold=0.25,
            target_class="person",
            model=model,
        )

        detection = detector.detect(image)

        self.assertTrue(detection.is_tracking)
        self.assertEqual("person", detection.label)
        self.assertEqual([(image, False)], model.calls)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the adapter tests to verify RED**

Run:

```bash
source /opt/ros/jazzy/setup.bash
PYTHONPATH=src/robot_perception:$PYTHONPATH python3 -m unittest src/robot_perception/test/test_yolo_detector.py
```

Expected: FAIL with `ModuleNotFoundError: No module named 'robot_perception.yolo_detector'`.

- [ ] **Step 3: Implement the minimal YOLO adapter**

Create `src/robot_perception/robot_perception/yolo_detector.py` with:

```python
from robot_perception.color_blob_detector import DetectionResult, empty_detection


class YoloDetectorDependencyError(RuntimeError):
    """Raised when the YOLO backend is requested but Ultralytics is unavailable."""


def _as_list(value):
    if hasattr(value, "detach"):
        value = value.detach()
    if hasattr(value, "cpu"):
        value = value.cpu()
    if hasattr(value, "numpy"):
        value = value.numpy()
    if hasattr(value, "tolist"):
        return value.tolist()
    return list(value)


def _class_name(result, class_id):
    names = getattr(result, "names", {})
    if isinstance(names, dict):
        return names.get(class_id, str(class_id))
    if isinstance(names, (list, tuple)) and 0 <= class_id < len(names):
        return names[class_id]
    return str(class_id)


def detection_from_yolo_result(
    result,
    image_shape,
    confidence_threshold: float,
    target_class: str = "",
) -> DetectionResult:
    boxes = getattr(result, "boxes", None)
    if boxes is None:
        return empty_detection()

    xyxy_values = _as_list(boxes.xyxy)
    confidence_values = _as_list(boxes.conf)
    class_values = _as_list(boxes.cls)
    image_height, image_width = image_shape[:2]

    best_detection = empty_detection()
    best_confidence = confidence_threshold

    for xyxy, confidence, class_value in zip(xyxy_values, confidence_values, class_values):
        confidence = float(confidence)
        if confidence < best_confidence:
            continue

        class_id = int(class_value)
        label = _class_name(result, class_id)
        if target_class and label != target_class:
            continue

        x_min, y_min, x_max, y_max = [float(value) for value in xyxy]
        width = max(0.0, x_max - x_min)
        height = max(0.0, y_max - y_min)
        if width <= 0.0 or height <= 0.0:
            continue

        best_confidence = confidence
        best_detection = DetectionResult(
            label=label,
            confidence=confidence,
            center_x=((x_min + x_max) / 2.0) / image_width,
            center_y=((y_min + y_max) / 2.0) / image_height,
            width=width / image_width,
            height=height / image_height,
            is_tracking=True,
        )

    return best_detection


class YoloObjectDetector:
    """Runs one Ultralytics YOLO model and returns the best DetectionResult."""

    def __init__(
        self,
        model_path: str,
        confidence_threshold: float = 0.25,
        target_class: str = "",
        model=None,
    ):
        self.model = model if model is not None else self._load_model(model_path)
        self.confidence_threshold = confidence_threshold
        self.target_class = target_class

    def detect(self, image) -> DetectionResult:
        results = self.model(image, verbose=False)
        if not results:
            return empty_detection()
        return detection_from_yolo_result(
            results[0],
            image.shape,
            confidence_threshold=self.confidence_threshold,
            target_class=self.target_class,
        )

    def _load_model(self, model_path: str):
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise YoloDetectorDependencyError(
                "YOLO backend requires ultralytics. Activate the WSL YOLO environment "
                "or install it with: python3 -m pip install ultralytics"
            ) from exc
        return YOLO(model_path)
```

- [ ] **Step 4: Run adapter tests to verify GREEN**

Run:

```bash
source /opt/ros/jazzy/setup.bash
PYTHONPATH=src/robot_perception:$PYTHONPATH python3 -m unittest src/robot_perception/test/test_yolo_detector.py
```

Expected: PASS.

## Task 2: Node Backend Selection

**Files:**
- Modify: `src/robot_perception/robot_perception/image_detector_node.py`
- Modify: `src/robot_perception/test/test_perception_assets.py`

- [ ] **Step 1: Write failing asset tests for backend parameters**

Extend `test_package_files_exist` in `src/robot_perception/test/test_perception_assets.py` with:

```python
self.assertTrue((PACKAGE_ROOT / "robot_perception" / "yolo_detector.py").is_file())
self.assertTrue((PACKAGE_ROOT / "config" / "yolo_detector.yaml").is_file())
self.assertTrue((PACKAGE_ROOT / "launch" / "yolo_detector.launch.py").is_file())
self.assertTrue((PACKAGE_ROOT / "WEEK_05_02_YOLO_BACKEND.md").is_file())
```

Extend `test_config_uses_camera_image_and_target_detection_topics` with:

```python
self.assertIn("detector_backend: color", config_text)
```

Extend `test_image_detector_node_uses_cv_bridge_sensor_qos_and_target_message` with:

```python
self.assertIn("detector_backend", node_source)
self.assertIn("YoloObjectDetector", node_source)
self.assertIn("yolo_model_path", node_source)
self.assertIn("yolo_confidence_threshold", node_source)
self.assertIn("yolo_target_class", node_source)
```

- [ ] **Step 2: Run asset tests to verify RED**

Run:

```bash
source /opt/ros/jazzy/setup.bash
PYTHONPATH=src/robot_perception:$PYTHONPATH python3 -m unittest src/robot_perception/test/test_perception_assets.py
```

Expected: FAIL because YOLO config, launch, handout, and node strings are missing.

- [ ] **Step 3: Modify `image_detector_node.py`**

Add the import:

```python
from robot_perception.yolo_detector import YoloObjectDetector
```

Declare and read the new parameters:

```python
self.declare_parameter("detector_backend", "color")
self.declare_parameter("yolo_model_path", "yolov8n.pt")
self.declare_parameter("yolo_confidence_threshold", 0.25)
self.declare_parameter("yolo_target_class", "")

self.detector_backend = self.get_parameter("detector_backend").value
self.yolo_detector = None
if self.detector_backend == "yolo":
    self.yolo_detector = YoloObjectDetector(
        model_path=self.get_parameter("yolo_model_path").value,
        confidence_threshold=float(self.get_parameter("yolo_confidence_threshold").value),
        target_class=self.get_parameter("yolo_target_class").value,
    )
elif self.detector_backend != "color":
    raise ValueError(f"Unsupported detector_backend: {self.detector_backend}")
```

Replace the color-only detection block in `image_callback` with:

```python
if self.detector_backend == "yolo":
    detection = self.yolo_detector.detect(cv_image)
else:
    detection = detect_largest_color_blob(
        cv_image,
        target_color=self.target_color,
        min_area_pixels=self.min_area_pixels,
    )
```

- [ ] **Step 4: Run existing node shutdown tests**

Run:

```bash
source /opt/ros/jazzy/setup.bash
PYTHONPATH=src/robot_perception:$PYTHONPATH python3 -m unittest src/robot_perception/test/test_node_shutdown.py
```

Expected: PASS.

## Task 3: YOLO Launch, Config, and Handout

**Files:**
- Modify: `src/robot_perception/config/color_detector.yaml`
- Create: `src/robot_perception/config/yolo_detector.yaml`
- Create: `src/robot_perception/launch/yolo_detector.launch.py`
- Create: `src/robot_perception/WEEK_05_02_YOLO_BACKEND.md`
- Modify: `src/robot_perception/README.md`
- Modify: `README.md`
- Modify: `ros2_learning_notes.md`

- [ ] **Step 1: Add `detector_backend` to color config**

Add this under `ros__parameters` in `src/robot_perception/config/color_detector.yaml`:

```yaml
detector_backend: color
```

- [ ] **Step 2: Create YOLO config**

Create `src/robot_perception/config/yolo_detector.yaml`:

```yaml
image_detector_node:
  ros__parameters:
    use_sim_time: true
    image_topic: /camera/image_raw
    detection_topic: /target_detection
    debug_image_topic: /target_detection/debug_image
    publish_debug_image: true
    detector_backend: yolo
    target_color: red
    min_area_pixels: 200.0
    yolo_model_path: yolov8n.pt
    yolo_confidence_threshold: 0.25
    yolo_target_class: ""
```

- [ ] **Step 3: Create YOLO launch**

Create `src/robot_perception/launch/yolo_detector.launch.py` by mirroring `color_detector.launch.py`, loading `yolo_detector.yaml`, and exposing launch arguments:

```python
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    perception_share = Path(get_package_share_directory("robot_perception"))
    config_path = perception_share / "config" / "yolo_detector.yaml"

    use_sim_time = LaunchConfiguration("use_sim_time")
    yolo_model_path = LaunchConfiguration("yolo_model_path")
    yolo_confidence_threshold = LaunchConfiguration("yolo_confidence_threshold")
    yolo_target_class = LaunchConfiguration("yolo_target_class")

    return LaunchDescription(
        [
            DeclareLaunchArgument("use_sim_time", default_value="true"),
            DeclareLaunchArgument("yolo_model_path", default_value="yolov8n.pt"),
            DeclareLaunchArgument("yolo_confidence_threshold", default_value="0.25"),
            DeclareLaunchArgument("yolo_target_class", default_value=""),
            Node(
                package="robot_perception",
                executable="image_detector_node",
                name="image_detector_node",
                output="screen",
                parameters=[
                    str(config_path),
                    {"use_sim_time": use_sim_time},
                    {"yolo_model_path": yolo_model_path},
                    {"yolo_confidence_threshold": yolo_confidence_threshold},
                    {"yolo_target_class": yolo_target_class},
                ],
            ),
        ]
    )
```

- [ ] **Step 4: Write the lesson handout**

Create `src/robot_perception/WEEK_05_02_YOLO_BACKEND.md` with sections:

```markdown
# 第 5 周第 2 小课：接入真实 YOLO 后端

本课目标：

- 在 WSL/Ubuntu 的 ROS 2 环境内安装并使用 Ultralytics YOLO。
- 让同一个 `image_detector_node` 支持 `detector_backend:=color|yolo`。
- 继续发布 `/target_detection` 和 `/target_detection/debug_image`。

## 一、为什么继续复用同一个节点

第 1 小课已经验证了 ROS 2 图像订阅、QoS、`cv_bridge`、自定义消息和 debug 图像发布。
本课只替换检测算法后端，避免重复节点代码。

## 二、准备 WSL YOLO 环境

推荐使用带 ROS 系统包可见性的 venv：

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
python3 -m venv .venv_yolo --system-site-packages
source .venv_yolo/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install ultralytics
```

## 三、构建

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
source .venv_yolo/bin/activate
python3 -m colcon build --packages-select robot_interfaces robot_simulation robot_perception
source install/setup.bash
```

## 四、运行

终端 1：

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
source .venv_yolo/bin/activate
source install/setup.bash
ros2 launch robot_simulation diffbot_sensors_rviz.launch.py
```

终端 2：

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
source .venv_yolo/bin/activate
source install/setup.bash
ros2 launch robot_perception yolo_detector.launch.py
ros2 topic echo /target_detection
```
```

- [ ] **Step 5: Update README files and learning notes**

Add the YOLO launch entry to:

```text
src/robot_perception/README.md
README.md
ros2_learning_notes.md
```

- [ ] **Step 6: Run asset tests to verify GREEN**

Run:

```bash
source /opt/ros/jazzy/setup.bash
PYTHONPATH=src/robot_perception:$PYTHONPATH python3 -m unittest src/robot_perception/test/test_perception_assets.py
```

Expected: PASS.

## Task 4: Full Verification and Context Update

**Files:**
- Modify: `CODEX_CONTEXT.md`

- [ ] **Step 1: Run all robot_perception unit tests**

Run:

```bash
source /opt/ros/jazzy/setup.bash
PYTHONPATH=src/robot_perception:$PYTHONPATH python3 -m unittest discover -s src/robot_perception/test
```

Expected: all tests pass.

- [ ] **Step 2: Run syntax checks**

Run:

```bash
python3 -m compileall src/robot_perception
```

Expected: compile succeeds.

- [ ] **Step 3: Build ROS packages**

Run:

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select robot_interfaces robot_perception
```

Expected: build succeeds.

- [ ] **Step 4: Verify launch arguments**

Run:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ROS_LOG_DIR=/tmp/ros2_launch_logs ros2 launch robot_perception yolo_detector.launch.py --show-args
```

Expected: output lists `use_sim_time`, `yolo_model_path`, `yolo_confidence_threshold`, and `yolo_target_class`.

- [ ] **Step 5: Update context handoff**

Append a new dated entry to `CODEX_CONTEXT.md` covering:

```text
第 5 周第 2 小课：同一个 image_detector_node 已支持 detector_backend:=color|yolo。
新增 yolo_detector.py、yolo_detector.yaml、yolo_detector.launch.py 和 WEEK_05_02_YOLO_BACKEND.md。
WSL YOLO 运行建议使用 .venv_yolo --system-site-packages。
```

- [ ] **Step 6: Review final diff**

Run:

```bash
git diff --stat
git diff --check
git status --short --branch
```

Expected: no whitespace errors, only task-related files changed.
