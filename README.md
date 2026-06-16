# ROS 2 学习仓库

这个仓库用于记录 ROS 2 学习笔记，并保存每周的小练习代码。

## 当前环境建议

- Ubuntu 24.04 LTS
- ROS 2 Jazzy Jalisco

## 目录结构

```text
.
├── ros2_learning_notes.md
└── src/
    ├── robot_bringup/
    ├── robot_description/
    ├── robot_interfaces/
    ├── robot_simulation/
    ├── tf2_frame_demo/
    └── turtlesim_p_controller/
```

## 第一个练习

`src/turtlesim_p_controller` 是第 1 周练习：用 P 控制让 turtlesim 乌龟移动到固定目标点。

本地纯 Python 测试：

```bash
PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test
```

安装 ROS 2 Jazzy 后运行：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select turtlesim_p_controller
source install/setup.bash
```

终端 1：

```bash
ros2 run turtlesim turtlesim_node
```

终端 2：

```bash
ros2 run turtlesim_p_controller turtle_goal_controller
```

第 2 周开始，也可以用 launch 文件一次启动两个节点：

```bash
ros2 launch turtlesim_p_controller turtlesim_goal.launch.py
```

创建 `robot_bringup` 包后，推荐用启动编排包作为系统入口：

```bash
colcon build --packages-select robot_interfaces turtlesim_p_controller robot_bringup
source install/setup.bash
ros2 launch robot_bringup turtlesim_goal.launch.py
```

第 2 周第 3 节加入自定义服务后，可以用它修改目标点：

```bash
ros2 service call /set_goal robot_interfaces/srv/SetGoal "{x: 2.0, y: 8.0}"
```

第 3 周第 1 节进入 tf2 和坐标系：

```bash
colcon build --packages-select tf2_frame_demo
source install/setup.bash
ros2 launch tf2_frame_demo tf2_demo.launch.py
```

查看 `map -> camera_link`：

```bash
ros2 run tf2_ros tf2_echo map camera_link
```

用 RViz2 观察 TF 坐标轴：

```bash
rviz2
```

打开后设置 `Fixed Frame = map`，再添加 `TF` display。

第 3 周第 2 节进入 `robot_description` 和 URDF，第 3 节把模型升级为 Xacro 并接入 bringup：

```bash
colcon build --packages-select robot_description robot_bringup
source install/setup.bash
ros2 launch robot_bringup display_robot.launch.py
```

也可以直接启动模型包入口：

```bash
ros2 launch robot_description display.launch.py
```

这个 launch 会启动 `robot_state_publisher` 和 RViz2，用 `src/robot_description/urdf/diffbot.urdf.xacro` 生成简化差速小车模型，并观察：

```text
base_link
left_wheel_link
right_wheel_link
camera_link
camera_optical_frame
laser_link
```

单独检查 Xacro 展开：

```bash
xacro src/robot_description/urdf/diffbot.urdf.xacro
```

第 4 周进入 Gazebo 仿真。先确认是否安装 Gazebo Harmonic 和 ROS-Gazebo bridge：

```bash
source /opt/ros/jazzy/setup.bash
command -v gz
ros2 pkg prefix ros_gz_sim
ros2 pkg prefix ros_gz_bridge
```

如果 `ros_gz_sim` 或 `ros_gz_bridge` 找不到，先安装：

```bash
sudo apt update
sudo apt install ros-jazzy-ros-gz
```

启动第 4 周第 1 小课的 Gazebo 空世界和 `/clock` bridge：

```bash
colcon build --packages-select robot_simulation
source install/setup.bash
ros2 launch robot_simulation gazebo_empty_world.launch.py
```

另开终端检查仿真时间是否桥接到 ROS 2：

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 topic echo /clock --once
```

第 4 周第 2 小课启动可运动差速小车：

```bash
colcon build --packages-select robot_simulation
source install/setup.bash
ros2 launch robot_simulation diffbot_drive.launch.py
```

另开终端发送速度命令并查看里程计：

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.25}, angular: {z: 0.0}}"
ros2 topic echo /odom --once
```

第 4 周第 3 小课启动雷达、相机、TF 和 RViz 同步显示：

```bash
colcon build --packages-select robot_description robot_simulation
source install/setup.bash
ros2 launch robot_simulation diffbot_sensors_rviz.launch.py
```

另开终端用键盘控制小车：

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

常用按键：`i` 前进，`,` 后退，`j` 左转，`l` 右转，`k` 停止。

参数默认值在：

```text
src/turtlesim_p_controller/config/goal_controller.yaml
```

## Git 使用

查看状态：

```bash
git status --short --branch
```

查看改动：

```bash
git diff
```

提交：

```bash
git add README.md ros2_learning_notes.md src/turtlesim_p_controller
git commit -m "Add ROS 2 learning notes and turtlesim P controller"
```
