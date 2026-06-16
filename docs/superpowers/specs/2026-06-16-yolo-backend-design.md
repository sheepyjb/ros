# 第 5 周第 2 小课：真实 YOLO 后端接入设计

日期：2026-06-16

## 背景

第 5 周第 1 小课已经在 `robot_perception` 包内跑通了图像感知链路：

```text
/camera/image_raw -> image_detector_node -> /target_detection
                                      -> /target_detection/debug_image
```

现有节点使用 OpenCV 颜色检测作为后端，输出 `robot_interfaces/msg/TargetDetection`。第 2 小课的目标是在 WSL/Ubuntu 的 ROS 2 环境内接入真实 Ultralytics YOLO 后端，同时保留颜色检测作为无模型 fallback。

## 目标

- `image_detector_node` 支持参数 `detector_backend:=color|yolo`。
- `color` 后端继续使用现有 `color_blob_detector.py`。
- 新增 `robot_perception/yolo_detector.py`，只负责把 Ultralytics YOLO 推理结果转换成现有 `DetectionResult`。
- 继续发布单个最高优先级目标到 `/target_detection`。
- 继续发布画框后的 `/target_detection/debug_image`。
- 新增 YOLO 专用 launch/config 和课程讲义。

## 非目标

- 不修改 `TargetDetection.msg` 为数组消息。
- 不在本课实现多目标跟踪。
- 不接 Windows `D:\pytorch` 环境或跨系统服务后端。
- 不引入 Nav2、控制节点或 rosbag2 正式练习。

## 方案

采用同一个 `image_detector_node`，通过 `detector_backend` 参数选择检测后端。

推荐理由：

- 保留第 1 小课已验证的 ROS 图像订阅、QoS、消息发布和 debug 图像发布逻辑。
- 颜色检测仍可在没有 YOLO 模型或依赖时作为教学 fallback。
- YOLO 只作为算法适配层加入，减少重复节点代码。

## 组件边界

### `image_detector_node.py`

职责：

- 订阅 `sensor_msgs/msg/Image`。
- 使用 `cv_bridge` 转成 OpenCV BGR 图像。
- 根据 `detector_backend` 调用颜色后端或 YOLO 后端。
- 将 `DetectionResult` 转成 `TargetDetection`。
- 发布 debug 图像。

新增参数：

```text
detector_backend: color | yolo
yolo_model_path: YOLO 权重路径或模型名
yolo_confidence_threshold: 最小置信度
yolo_target_class: 目标类别名，空字符串表示接受任意类别
```

### `yolo_detector.py`

职责：

- 延迟导入 `ultralytics.YOLO`，避免未安装 YOLO 时影响颜色检测和普通单元测试。
- 加载指定模型。
- 对单帧 BGR 图像执行推理。
- 在结果中选择置信度最高且满足类别过滤的目标。
- 输出 `DetectionResult`，坐标仍为归一化 `center_x/center_y/width/height`。

### Launch 和配置

- 保留 `color_detector.launch.py` 和 `color_detector.yaml`。
- 新增 `yolo_detector.launch.py` 和 `yolo_detector.yaml`。
- YOLO launch 默认设置 `detector_backend:=yolo`。

## 错误处理

- 如果 `detector_backend` 不是 `color` 或 `yolo`，节点启动时报清楚错误。
- 如果选择 `yolo` 但未安装 `ultralytics`，只在初始化 YOLO 后端时报错，并提示安装依赖。
- 如果 YOLO 当前帧没有检测到目标，发布空检测结果，`is_tracking=false`。
- 如果 `yolo_target_class` 不为空但当前帧没有该类别，也发布空检测结果。

## 测试策略

先按 TDD 增加测试：

- 用 fake YOLO model 测试 `yolo_detector.py` 能把像素框转换成归一化 `DetectionResult`。
- 测试低于置信度阈值的结果会被忽略。
- 测试类别过滤只接受指定类别。
- 测试没有结果时返回 empty detection。
- 资产测试覆盖新增 `yolo_detector.py`、`yolo_detector.yaml`、`yolo_detector.launch.py` 和第 2 小课讲义。
- 节点清理逻辑继续沿用已有 `test_node_shutdown.py`。

验证命令：

```bash
source /opt/ros/jazzy/setup.bash
PYTHONPATH=src/robot_perception:$PYTHONPATH python3 -m unittest discover -s src/robot_perception/test
python3 -m compileall src/robot_perception
colcon build --packages-select robot_interfaces robot_perception
ros2 launch robot_perception yolo_detector.launch.py --show-args
```

实际运行时，还需要在 WSL 的 ROS 2 Python 环境中安装 `ultralytics` 和可用模型权重。
