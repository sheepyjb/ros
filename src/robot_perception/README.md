# robot_perception

第 5 周开始使用这个包保存 ROS 2 图像感知节点。

当前职责：

- `robot_perception/color_blob_detector.py`：纯 OpenCV 颜色目标检测逻辑。
- `robot_perception/image_detector_node.py`：订阅 `/camera/image_raw`，发布 `/target_detection` 和 `/target_detection/debug_image`。
- `config/`：感知节点默认参数。
- `launch/`：感知节点启动入口。

第 5 周第 1 小课入口：

```bash
ros2 launch robot_simulation diffbot_sensors_rviz.launch.py
ros2 launch robot_perception color_detector.launch.py
```
