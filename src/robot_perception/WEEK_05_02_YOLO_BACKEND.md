# 第 5 周第 2 小课：接入真实 YOLO 后端

这份文档对应第 5 周第 2 小课：在 WSL/Ubuntu 的 ROS 2 环境内使用 Ultralytics YOLO，把第 1 小课的颜色检测后端替换成真实目标检测后端。

本课目标：

- 在 WSL 内准备能同时访问 ROS 2 包和 YOLO 依赖的 Python 环境。
- 让同一个 `image_detector_node` 支持 `detector_backend:=color|yolo`。
- 继续发布 `robot_interfaces/msg/TargetDetection` 到 `/target_detection`。
- 继续发布 `/target_detection/debug_image`，方便在 RViz2 中观察检测框。

## 一、为什么复用同一个节点

第 5 周第 1 小课已经验证了：

- `/camera/image_raw` 图像订阅。
- `cv_bridge` 图像转换。
- sensor data QoS。
- `TargetDetection.msg` 发布。
- debug 图像发布。

本课只替换检测算法后端。这样可以把问题范围缩小到 YOLO 模型加载和推理结果转换，而不是重新写一套 ROS 2 节点。

## 二、本课数据流

```text
Gazebo camera
  -> /camera/image_raw
  -> image_detector_node
  -> YOLO backend
  -> /target_detection
  -> /target_detection/debug_image
```

`/target_detection` 的消息格式不变，仍然只发布当前最优的单个目标。

## 三、准备 WSL YOLO 环境

不要使用 Windows 的 `D:\pytorch` 环境直接运行 ROS 2 节点。本课选择在 WSL 内安装 YOLO 依赖。

推荐创建一个能看到 ROS 2 系统包的 venv：

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
python3 -m venv .venv_yolo --system-site-packages
source .venv_yolo/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install ultralytics
```

检查依赖：

```bash
python3 -c "import ultralytics; import rclpy; import cv_bridge; print('yolo ros env ok')"
```

如果这个命令通过，说明同一个 Python 环境既能导入 YOLO，也能导入 ROS 2 Python 包。

## 四、构建

激活 `.venv_yolo` 后构建，确保安装出来的 Python 入口使用这个环境：

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
source .venv_yolo/bin/activate
python3 -m colcon build --packages-select robot_interfaces robot_simulation robot_perception
source install/setup.bash
```

## 五、终端 1：启动仿真和相机

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
source .venv_yolo/bin/activate
source install/setup.bash
ros2 launch robot_simulation diffbot_sensors_rviz.launch.py
```

确认图像话题存在：

```bash
ros2 topic list | grep /camera/image_raw
```

## 六、终端 2：启动 YOLO 检测节点

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
source .venv_yolo/bin/activate
source install/setup.bash
ros2 launch robot_perception yolo_detector.launch.py
```

查看检测结果：

```bash
ros2 topic echo /target_detection
```

首次使用 `yolov8n.pt` 时，Ultralytics 可能会联网下载模型权重。后续也可以换成本地权重路径：

```bash
ros2 launch robot_perception yolo_detector.launch.py yolo_model_path:=/home/sheepyjb/models/my_yolo.pt
```

## 七、参数

默认参数在：

```text
src/robot_perception/config/yolo_detector.yaml
```

关键参数：

- `detector_backend`：检测后端，本课为 `yolo`。
- `yolo_model_path`：模型名或本地权重路径，默认 `yolov8n.pt`。
- `yolo_confidence_threshold`：低于该置信度的框会被忽略，默认 `0.25`。
- `yolo_target_class`：只保留指定类别；空字符串表示接受任意类别。
- `publish_debug_image`：是否发布画框后的图像。

只检测 `person` 类别：

```bash
ros2 launch robot_perception yolo_detector.launch.py yolo_target_class:=person
```

提高置信度阈值：

```bash
ros2 launch robot_perception yolo_detector.launch.py yolo_confidence_threshold:=0.5
```

## 八、在 RViz2 中看 debug 图像

在 RViz2 中添加 Image display：

```text
Add -> By topic -> /target_detection/debug_image
```

如果 YOLO 检测到目标，debug 图像会显示黄色检测框和类别名。

## 九、练习

练习 1：创建并激活 `.venv_yolo`，确认 `ultralytics`、`rclpy` 和 `cv_bridge` 都能导入。

练习 2：启动仿真，确认 `/camera/image_raw` 存在。

练习 3：启动 `yolo_detector.launch.py`，观察 `/target_detection`。

练习 4：把 `yolo_confidence_threshold` 从 `0.25` 改成 `0.5`，观察低置信度目标是否更容易被忽略。

练习 5：设置 `yolo_target_class:=person`，观察非 person 类别是否被过滤。

## 十、知识问答

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
为什么 yolo_detector.py 要延迟导入 ultralytics？
```

参考答案：

```text
这样未安装 YOLO 依赖时，颜色检测后端和普通单元测试仍然能运行。
只有真正选择 detector_backend:=yolo 时，节点才需要加载 ultralytics 和模型权重。
```

问题 3：

```text
为什么本课仍然只发布单个 TargetDetection？
```

参考答案：

```text
后续目标跟随控制先只需要一个主目标。
保持消息合约不变可以减少本课变量，多目标数组和跟踪可以放到后续课程。
```

## 十一、通过标准

你可以进入下一小课的标准：

- 能解释 `detector_backend:=color|yolo` 的作用。
- 能在 WSL 内激活 `.venv_yolo` 并导入 `ultralytics`、`rclpy` 和 `cv_bridge`。
- 能启动 `robot_perception yolo_detector.launch.py`。
- 能 echo 到 `/target_detection`。
- 能在 RViz2 中看到 `/target_detection/debug_image`。
- 能解释 `yolo_confidence_threshold` 和 `yolo_target_class` 的作用。
