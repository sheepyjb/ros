# tf2_frame_demo

第 3 周第 1 小课示例包：用一个最小 TF 树理解 ROS 2 坐标系。

TF 树：

```text
map -> odom -> base_link -> camera_link
```

运行：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select tf2_frame_demo
source install/setup.bash
ros2 launch tf2_frame_demo tf2_demo.launch.py
```

查看 TF：

```bash
ros2 run tf2_ros tf2_echo map camera_link
ros2 run tf2_tools view_frames
```
