# 第 5 周第 1 小课：ROS 2 图像订阅与颜色目标检测

这份文档对应第 5 周第 1 小课：先不用真实 YOLO，先把 Gazebo 相机图像接入 ROS 2 感知节点，完成 `sensor_msgs/Image -> OpenCV -> TargetDetection` 的最小闭环。

本课目标：

- 理解 `/camera/image_raw` 是 `sensor_msgs/msg/Image`。
- 用 `cv_bridge` 把 ROS 图像转成 OpenCV BGR 图像。
- 用 OpenCV 找到画面里的红色目标。
- 发布 `robot_interfaces/msg/TargetDetection`。
- 发布 `/target_detection/debug_image`，方便在 RViz2 中观察检测框。

## 一、为什么先不直接上 YOLO

YOLO 依赖 `torch`、`ultralytics` 和模型权重。如果第一步直接接 YOLO，问题可能来自：

- ROS 2 图像订阅不对。
- `cv_bridge` 转换不对。
- QoS 不匹配。
- YOLO 依赖没装好。
- 模型类别和置信度阈值不合适。

本课先用 OpenCV 颜色检测替代 YOLO，目的是把 ROS 2 图像链路跑通。下一小课再把检测后端替换成真实 YOLO。

## 二、本课数据流

```text
Gazebo camera
  -> /camera/image_raw
  -> image_detector_node
  -> /target_detection
  -> /target_detection/debug_image
```

其中：

- `/camera/image_raw` 来自第 4 周 Gazebo 相机 bridge。
- `/target_detection` 使用第 2 周定义的 `TargetDetection.msg`。
- `/target_detection/debug_image` 是画好检测框的调试图像。

## 三、构建

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
colcon build --packages-select robot_interfaces robot_simulation robot_perception
source install/setup.bash
```

## 四、终端 1：启动仿真和相机

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
source install/setup.bash
ros2 launch robot_simulation diffbot_sensors_rviz.launch.py
```

启动后确认相机图像存在：

```bash
ros2 topic list | grep /camera/image_raw
ros2 topic info /camera/image_raw --verbose
```

## 五、终端 2：启动颜色检测节点

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
source install/setup.bash
ros2 launch robot_perception color_detector.launch.py
```

查看检测结果：

```bash
ros2 topic echo /target_detection
```

如果红色方块进入相机画面，应该能看到类似：

```text
label: red_target
confidence: 1.0
center_x: 0.5
center_y: 0.4
width: 0.2
height: 0.3
is_tracking: true
```

如果画面中没有足够大的红色目标，节点会发布：

```text
label: ''
confidence: 0.0
center_x: 0.0
center_y: 0.0
width: 0.0
height: 0.0
is_tracking: false
```

## 六、在 RViz2 中看 debug 图像

在第 4 周 RViz2 窗口里添加一个 Image display：

```text
Add -> By topic -> /target_detection/debug_image
```

如果检测成功，debug 图像会在红色目标外画黄色框。

## 七、参数

默认参数在：

```text
src/robot_perception/config/color_detector.yaml
```

关键参数：

- `image_topic`：输入图像，默认 `/camera/image_raw`。
- `detection_topic`：检测结果，默认 `/target_detection`。
- `debug_image_topic`：调试图像，默认 `/target_detection/debug_image`。
- `target_color`：检测颜色，当前支持 `red` 和 `green`。
- `min_area_pixels`：最小目标面积，过小会被当成噪声。
- `publish_debug_image`：是否发布画框后的图像。

临时检测绿色圆柱：

```bash
ros2 launch robot_perception color_detector.launch.py target_color:=green
```

如果要长期修改默认值，可以直接编辑 YAML。

## 八、练习

练习 1：启动仿真，确认 ROS 2 能看到 `/camera/image_raw`。

练习 2：启动 `image_detector_node`，用 `ros2 topic echo /target_detection` 观察检测结果。

练习 3：在 RViz2 中添加 `/target_detection/debug_image`，观察检测框。

练习 4：把 `target_color` 改成 `green`，观察绿色圆柱是否能被检测。

练习 5：把 `min_area_pixels` 从 `200.0` 改成更大的值，观察小目标是否更容易被忽略。

## 九、知识问答

问题 1：

```text
为什么本课先用 OpenCV 颜色检测，而不是直接上 YOLO？
```

参考答案：

```text
因为颜色检测能先验证 ROS 2 图像订阅、cv_bridge 转换、QoS、检测消息发布和 debug 图像发布。
如果这条链路不通，直接上 YOLO 时很难判断问题来自 ROS 2 还是深度学习依赖。
```

问题 2：

```text
TargetDetection.msg 里的 center_x、center_y、width、height 为什么用归一化坐标？
```

参考答案：

```text
归一化坐标和图像分辨率无关。
例如 center_x=0.5 永远表示画面水平中心，后续控制节点不需要关心相机是 640x480 还是 1280x720。
```

问题 3：

```text
为什么图像订阅要使用 sensor data QoS？
```

参考答案：

```text
相机图像是高频传感器数据，通常更关注最新帧，而不是保证每一帧都可靠送达。
sensor data QoS 更适合这类实时传感器话题，也更容易和 Gazebo bridge 的传感器话题匹配。
```

## 十、通过标准

你可以进入下一小课的标准：

- 能启动 `robot_simulation diffbot_sensors_rviz.launch.py`。
- 能启动 `robot_perception color_detector.launch.py`。
- 能 echo 到 `/target_detection`。
- 能解释 `sensor_msgs/Image`、`cv_bridge`、OpenCV 图像和 `TargetDetection.msg` 的关系。
- 能在 RViz2 中看到 `/target_detection/debug_image`。
