# 第 5 周第 2 小课：接入真实 YOLO 后端

本课把第 5 周第 1 小课的颜色检测扩展成真实 YOLO 检测：仍然复用同一个 `image_detector_node`，但通过参数把检测后端切到 `yolo`。

本课跑通后的效果：

- Gazebo 发布 `/camera/image_raw`。
- `image_detector_node` 使用 Ultralytics YOLO 推理。
- `/target_detection` 发布一个最优目标。
- `/target_detection/debug_image` 发布带检测框的调试图像。
- 当前仿真世界内的 STOP 标志牌可以被默认 `yolov8n.pt` 识别为 `stop sign`。

## 一、本课目标

完成后你应该能做到：

- 在 WSL 内准备 YOLO + ROS 2 共用的 Python 环境。
- 解释 `detector_backend:=color|yolo` 的作用。
- 启动 Gazebo 相机，再启动 YOLO 感知节点。
- 在 RViz2 Image 面板看到 STOP 牌和黄色检测框。
- 用 `ros2 topic echo /target_detection` 看到 YOLO 检测结果。
- 处理本课常见环境问题：`python3-venv` 缺失、`ultralytics` 找不到、pip 下载中断、旧 Gazebo 进程、CUDA warning。

## 二、为什么复用同一个节点

第 5 周第 1 小课已经验证了图像感知节点的 ROS 外壳：

- 订阅 `/camera/image_raw`。
- 使用 `cv_bridge` 做 ROS Image 和 OpenCV 图像转换。
- 发布 `robot_interfaces/msg/TargetDetection` 到 `/target_detection`。
- 发布 `/target_detection/debug_image` 供 RViz2 观察。

本课只替换算法后端，不改消息合约和话题名。这样第 6 周做目标跟随时，不需要关心目标来自颜色检测还是 YOLO。

## 三、本课数据流

```text
Gazebo camera
  -> /camera/image_raw
  -> image_detector_node
  -> detector_backend=yolo
  -> YoloObjectDetector
  -> /target_detection
  -> /target_detection/debug_image
```

`/target_detection` 仍然只发布当前最优的单个目标。多目标数组、跟踪 ID、深度估计先不放进本课。

## 四、代码结构

关键文件：

```text
src/robot_perception/robot_perception/image_detector_node.py
src/robot_perception/robot_perception/yolo_detector.py
src/robot_perception/config/yolo_detector.yaml
src/robot_perception/launch/yolo_detector.launch.py
src/robot_simulation/worlds/diffbot_sensors.world.sdf
src/robot_simulation/materials/textures/yolo_stop_sign.png
```

职责划分：

- `image_detector_node.py`：ROS 2 节点外壳，负责订阅图像、读取参数、发布检测结果和 debug 图。
- `yolo_detector.py`：只负责运行 Ultralytics YOLO，并把 YOLO 输出转换成现有 `DetectionResult`。
- `yolo_detector.yaml`：把同一个节点切到 `detector_backend: yolo`。
- `yolo_detector.launch.py`：暴露 `yolo_model_path`、`yolo_confidence_threshold`、`yolo_target_class` 等运行参数。
- `diffbot_sensors.world.sdf`：放置 Gazebo 相机、机器人、障碍物和 YOLO 可识别的 STOP 标志牌。

`yolo_detector.py` 延迟导入 `ultralytics`。这样没安装 YOLO 依赖时，颜色检测后端和普通单元测试仍然能运行；只有真的选择 `detector_backend:=yolo` 时才加载模型。

## 五、一次性准备 WSL YOLO 环境

不要直接用 Windows 的 `D:\pytorch` 环境运行 ROS 2 节点。本课的 ROS 2、Gazebo、`rclpy`、`cv_bridge` 都在 WSL 内，所以 YOLO 也放在 WSL 内跑。

第一次配置 WSL 环境：

```bash
cd /home/sheepyjb/ros

sudo apt update
sudo apt install python3.12-venv python3-pip

source /opt/ros/jazzy/setup.bash
rm -rf .venv_yolo
python3 -m venv .venv_yolo --system-site-packages
source .venv_yolo/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install --no-cache-dir --timeout 300 --retries 20 \
  -i https://pypi.tuna.tsinghua.edu.cn/simple \
  "numpy<2" ultralytics
```

说明：

- `python3.12-venv` 和 `python3-pip` 只需要安装一次。
- `.venv_yolo` 只需要创建一次。
- 以后每个新终端只需要 `source .venv_yolo/bin/activate`，不需要重新安装 ultralytics。
- `--system-site-packages` 很关键，它让 venv 能看到 ROS 2 apt 安装的 `rclpy`、`cv_bridge` 等 Python 包。
- `"numpy<2"` 用来保守避开部分 ROS Python 包和 NumPy 2 的兼容风险。
- 如果默认 PyPI 下载中断，可以继续用上面的清华源命令重试。

检查环境：

```bash
cd /home/sheepyjb/ros
source /opt/ros/jazzy/setup.bash
source .venv_yolo/bin/activate

python3 -c "import ultralytics, torch, rclpy, cv_bridge; print('yolo ros env ok', ultralytics.__version__, torch.__version__)"
```

能打印 `yolo ros env ok ...` 就说明同一个 Python 环境能同时导入 YOLO 和 ROS 2 Python 包。

## 六、构建

必须在激活 `.venv_yolo` 后构建，这样安装出来的 `image_detector_node` 入口脚本 shebang 会指向 `.venv_yolo/bin/python3`。

```bash
cd /home/sheepyjb/ros
source /opt/ros/jazzy/setup.bash
source .venv_yolo/bin/activate

python3 -m colcon build --packages-select robot_interfaces robot_simulation robot_perception
source install/setup.bash
```

检查入口脚本：

```bash
head -1 install/robot_perception/lib/robot_perception/image_detector_node
```

期望看到类似：

```text
#!/home/sheepyjb/ros/.venv_yolo/bin/python3
```

如果这里还是 `#!/usr/bin/python3`，YOLO launch 可能会报：

```text
ModuleNotFoundError: No module named 'ultralytics'
```

解决方式是重新激活 `.venv_yolo` 后再 build。

## 七、运行前检查旧进程

如果之前 Gazebo 自动关闭、TF 时间错乱、或者画面不是当前 world，先检查是否有旧进程：

```bash
ps -ef | rg 'gz sim|gazebo|rviz2|ros2 launch|image_detector_node|parameter_bridge|robot_state_publisher|odom_to_tf'
```

如果看到很早以前启动的 `gz sim`、`ros2 launch` 或 `image_detector_node`，先 Ctrl-C 对应终端。确实找不到终端时，再按 PID 清理：

```bash
kill <pid>
```

不要乱杀当前正在用的终端；只清理确定是旧的残留进程。

## 八、终端 1：启动仿真和 RViz2

```bash
cd /home/sheepyjb/ros
source /opt/ros/jazzy/setup.bash
source .venv_yolo/bin/activate
source install/setup.bash

ros2 launch robot_simulation diffbot_sensors_rviz.launch.py
```

启动后确认相机话题存在：

```bash
ros2 topic info /camera/image_raw
```

期望至少看到：

```text
Type: sensor_msgs/msg/Image
Publisher count: 1
```

当前 sensor 仿真世界里已经放了一个 STOP 标志牌。为了让牌子完整进入相机视野，`diffbot_sensors.world.sdf` 中的 `diffbot` 初始位姿放在：

```xml
<pose>-0.45 0 0 0 0 0</pose>
```

如果你只看 Gazebo 3D 视角，可能从背面或侧面看到黑色板面；本课验证以 RViz2 左侧 Image 面板的 `/camera/image_raw` 为准。相机侧应该能看到红色 STOP 牌。

## 九、终端 2：启动 YOLO 检测

推荐本课先只检测 STOP 标志牌：

```bash
cd /home/sheepyjb/ros
source /opt/ros/jazzy/setup.bash
source .venv_yolo/bin/activate
source install/setup.bash

ros2 launch robot_perception yolo_detector.launch.py yolo_target_class:="stop sign"
```

首次使用 `yolov8n.pt` 时，Ultralytics 可能会联网下载模型权重。下载后的 `.pt` 文件不要提交到 git，仓库已经通过 `.gitignore` 忽略 `*.pt`。

如果看到类似 warning：

```text
CUDA initialization: The NVIDIA driver on your system is too old ...
```

这表示当前 PyTorch CUDA 包发现宿主机 NVIDIA 驱动偏旧。它会回落到 CPU 跑，本课可以继续验证，只是推理速度可能慢一些。

## 十、终端 3：查看检测结果

检查 topic：

```bash
ros2 topic info /target_detection
ros2 topic info /target_detection/debug_image
```

查看检测结果：

```bash
ros2 topic echo --once /target_detection
```

一次实测结果如下：

```text
label: stop sign
confidence: 0.9717566967010498
center_x: 0.4991529583930969
center_y: 0.2337324470281601
width: 0.3895692527294159
height: 0.46462714672088623
is_tracking: true
```

字段含义：

- `label`：YOLO 类别名。
- `confidence`：YOLO 置信度。
- `center_x`、`center_y`：检测框中心点，按图像宽高归一化到 `0.0` 到 `1.0`。
- `width`、`height`：检测框宽高，同样是归一化值。
- `is_tracking`：本帧是否有有效目标；当前只是“检测到目标”，还不是多帧跟踪 ID。

在 RViz2 中看检测框：

```text
Add -> By topic -> /target_detection/debug_image
```

如果 YOLO 检测到目标，debug 图会显示黄色框和 `stop sign` 标签。

## 十一、参数

默认配置在：

```text
src/robot_perception/config/yolo_detector.yaml
```

关键参数：

- `detector_backend`：检测后端，`color` 或 `yolo`。本课配置为 `yolo`。
- `image_topic`：输入图像话题，默认 `/camera/image_raw`。
- `detection_topic`：结构化检测结果话题，默认 `/target_detection`。
- `debug_image_topic`：debug 图像话题，默认 `/target_detection/debug_image`。
- `yolo_model_path`：模型名或本地权重路径，默认 `yolov8n.pt`。
- `yolo_confidence_threshold`：低于该置信度的框会被忽略，默认 `0.25`。
- `yolo_target_class`：只保留指定类别；空字符串表示接受任意类别。
- `publish_debug_image`：是否发布画框后的图像。

只检测 STOP 牌：

```bash
ros2 launch robot_perception yolo_detector.launch.py yolo_target_class:="stop sign"
```

提高置信度阈值：

```bash
ros2 launch robot_perception yolo_detector.launch.py \
  yolo_target_class:="stop sign" \
  yolo_confidence_threshold:=0.5
```

换成本地权重：

```bash
ros2 launch robot_perception yolo_detector.launch.py \
  yolo_model_path:=/home/sheepyjb/models/my_yolo.pt
```

如果你以后训练了“红方块”权重，也可以把 `yolo_model_path` 指向自己的 `.pt`，并把 `yolo_target_class` 改成训练时的类别名。

## 十二、验证命令

静态验证：

```bash
cd /home/sheepyjb/ros
source /opt/ros/jazzy/setup.bash
source .venv_yolo/bin/activate

PYTHONPATH=src/robot_simulation:$PYTHONPATH python3 -m unittest discover -s src/robot_simulation/test
gz sdf -k src/robot_simulation/worlds/diffbot_sensors.world.sdf
python3 -m compileall src/robot_simulation
python3 -m colcon build --packages-select robot_simulation robot_perception
```

本次实测：

```text
17 tests OK
gz sdf: Valid.
compileall: passed
colcon build --packages-select robot_simulation robot_perception: passed
```

运行态验证：

```bash
ros2 topic info /camera/image_raw
ros2 topic info /target_detection
ros2 topic echo --once /target_detection
```

本次冷启动实测：

```text
/camera/image_raw: Publisher count 1
/target_detection: Publisher count 1
YOLO label: stop sign
YOLO confidence: 0.9717566967010498
is_tracking: true
```

## 十三、常见问题

### 1. `python3 -m venv` 报 ensurepip 不可用

症状：

```text
The virtual environment was not created successfully because ensurepip is not available.
```

原因：WSL Ubuntu 没装 venv 支持包。

修复：

```bash
sudo apt update
sudo apt install python3.12-venv python3-pip
rm -rf .venv_yolo
python3 -m venv .venv_yolo --system-site-packages
```

### 2. `python3: No module named pip`

原因：系统 pip 没装。

修复：

```bash
sudo apt install python3-pip
```

### 3. `ModuleNotFoundError: No module named 'ultralytics'`

优先检查：

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
source .venv_yolo/bin/activate
python3 -c "import ultralytics; print('ok')"
head -1 install/robot_perception/lib/robot_perception/image_detector_node
```

如果 `python3 -c` 能导入，但 launch 不能导入，通常是 build 时没激活 `.venv_yolo`，入口脚本 shebang 指到了系统 Python。重新激活 venv 后 build。

### 4. pip 下载到一半中断

症状：

```text
IncompleteRead
Connection broken
```

修复：

```bash
source .venv_yolo/bin/activate
python3 -m pip cache purge
python3 -m pip install --no-cache-dir --timeout 300 --retries 20 \
  -i https://pypi.tuna.tsinghua.edu.cn/simple \
  "numpy<2" ultralytics
```

### 5. colcon 提示 setuptools 版本冲突

你可能看到：

```text
colcon-core requires setuptools<80
```

如果 build 已经通过，本课可以继续。后续要彻底清理时，建议在 `.venv_yolo` 内把 setuptools 降到 `<80`，但不要在已经跑通的课堂验证中途随意重装环境。

### 6. Gazebo 或 RViz 自动关闭

先看 launch 输出。如果是你按 Ctrl-C，Gazebo 可能显示 `exit code -2`，这是正常的 SIGINT 退出。

如果不是手动退出，先查旧进程：

```bash
ps -ef | rg 'gz sim|gazebo|rviz2|ros2 launch|image_detector_node|parameter_bridge|robot_state_publisher|odom_to_tf'
```

本课已经把 `diffbot_sensors_rviz.launch.py` 的 `on_exit_shutdown` 改成 `false`，避免 Gazebo GUI wrapper 提前退出时把 RViz 和 bridge 一起带掉。

### 7. RViz 报 `TF_OLD_DATA`

常见原因是旧 Gazebo 进程还在发布旧 `/clock` 或旧 TF，导致新旧仿真时间混在一起。

处理顺序：

1. 停掉所有旧 launch 终端。
2. 用 `ps -ef | rg ...` 检查残留。
3. 确认干净后重新启动仿真。

### 8. Gazebo 里看到黑牌

本课检测以相机图像为准。请先看 RViz2 左侧 Image 面板或 `/camera/image_raw`，相机侧应该能看到红色 STOP 标志牌。

如果只在 Gazebo 3D 视角看，可能正好看到了牌子的背面、侧面或未刷新材质。YOLO 不看 Gazebo GUI 视角，它只看 `/camera/image_raw`。

### 9. STOP 牌被裁掉

当前 sensor world 已把机器人初始 x 坐标后移到 `-0.45`，冷启动时 STOP 牌能完整进入相机视野。

如果你手动移动过机器人，可以临时恢复：

```bash
gz service -s /world/diffbot_sensors_world/set_pose \
  --reqtype gz.msgs.Pose \
  --reptype gz.msgs.Boolean \
  --timeout 3000 \
  --req 'name: "diffbot" position { x: -0.45 y: 0 z: 0 } orientation { w: 1 }'
```

### 10. `ros2 topic echo --once /target_detection` 抢早失败

YOLO 首次加载模型会慢一些。先看 topic 是否存在：

```bash
ros2 topic info /target_detection
```

如果有 publisher，等几秒再 echo。

## 十四、练习

练习 1：创建并激活 `.venv_yolo`，确认 `ultralytics`、`torch`、`rclpy`、`cv_bridge` 都能导入。

练习 2：启动 `diffbot_sensors_rviz.launch.py`，确认 RViz2 Image 面板能看到 STOP 牌。

练习 3：启动 `yolo_detector.launch.py yolo_target_class:="stop sign"`，观察 `/target_detection`。

练习 4：把 `yolo_confidence_threshold` 从 `0.25` 改成 `0.5`，确认仍能检测 STOP 牌。

练习 5：把 `yolo_target_class` 改成 `"person"`，观察 `/target_detection` 如何变成未跟踪状态。

练习 6：不用启动 Gazebo，下一小课用 rosbag2 录制和回放 `/camera/image_raw`、`/target_detection`、`/target_detection/debug_image`，反复调阈值和类别过滤。

## 十五、知识问答

问题 1：

```text
为什么本课不直接使用 Windows 的 D:\pytorch 环境？
```

参考答案：

```text
因为 ROS 2 节点、rclpy、cv_bridge 和 Gazebo 相机话题都在 WSL 内。
如果跨到 Windows 环境，需要额外做进程通信、图像传输和结果回传，复杂度会明显增加。
```

问题 2：

```text
为什么要用 .venv_yolo --system-site-packages？
```

参考答案：

```text
YOLO 依赖来自 pip，但 rclpy、cv_bridge 等 ROS 2 Python 包来自 apt。
--system-site-packages 让 venv 既能安装 ultralytics，又能看到 ROS 2 系统包。
```

问题 3：

```text
为什么 yolo_detector.py 要延迟导入 ultralytics？
```

参考答案：

```text
这样未安装 YOLO 依赖时，颜色检测后端和普通单元测试仍然能运行。
只有真正选择 detector_backend:=yolo 时，节点才需要加载 ultralytics 和模型权重。
```

问题 4：

```text
为什么本课仍然只发布单个 TargetDetection？
```

参考答案：

```text
后续目标跟随控制先只需要一个主目标。
保持消息合约不变可以减少本课变量，多目标数组和跟踪 ID 可以放到后续课程。
```

问题 5：

```text
为什么仿真里选择 stop sign？
```

参考答案：

```text
默认 yolov8n.pt 是 COCO 预训练模型，原生认识 stop sign、person、car、bottle、chair 等类别。
在 Gazebo 里放一个 stop sign，可以不用训练自己的模型就验证真实 YOLO 后端。
```

## 十六、通过标准

可以进入第 5 周第 3 小课的标准：

- 能解释 `detector_backend:=color|yolo`。
- 能在 WSL 内激活 `.venv_yolo` 并导入 `ultralytics`、`torch`、`rclpy`、`cv_bridge`。
- 能确认 `image_detector_node` 的 shebang 指向 `.venv_yolo/bin/python3`。
- 能启动 `robot_simulation diffbot_sensors_rviz.launch.py`。
- 能启动 `robot_perception yolo_detector.launch.py yolo_target_class:="stop sign"`。
- 能 echo 到 `/target_detection`，并看到 `label: stop sign`、`is_tracking: true`。
- 能在 RViz2 中看到 `/target_detection/debug_image` 的黄色检测框。
- 能说明当前仿真为什么用 STOP 标志牌验证默认 COCO YOLO 模型。
- 能处理本课常见问题中的至少三类环境或运行问题。

下一小课建议：`rosbag2` 感知数据录制与回放调试。录制 `/camera/image_raw`、`/target_detection`、`/target_detection/debug_image`，以后不用每次启动 Gazebo，也能反复回放同一段图像来调 YOLO 阈值和类别过滤。
