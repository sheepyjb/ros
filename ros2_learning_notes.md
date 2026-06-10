# ROS 2 学习笔记

## 当前选择

- 系统建议：Ubuntu 24.04 LTS。
- ROS 2 建议：ROS 2 Jazzy Jalisco。
- 原因：Jazzy 是 Ubuntu 24.04 的主支持发行版，官方 deb 包、教程、Gazebo/Nav2/MoveIt2 资料和第三方包兼容性更适合学习。
- 暂不建议：Ubuntu 26.04 + ROS 2 Lyrical 作为第一套学习环境。Lyrical 更新，但第三方生态需要时间跟上。

## 总目标

用 8 到 10 周完成一个小型机器人系统：

> 在仿真中搭建差速小车，接入摄像头和雷达，使用 YOLO 做目标检测，用 Nav2 做导航，用控制节点完成目标跟随、避障或接近任务，并能用 RViz 与 rosbag2 调试全过程。

## 学习路线

### 第 1 周：ROS 2 基础通信

目标：理解 ROS 2 的节点、话题、服务、动作、参数，以及如何用命令行观察系统。

要学：

- `ros2 node`
- `ros2 topic`
- `ros2 service`
- `ros2 action`
- `ros2 param`
- `rqt_graph`
- `turtlesim`

练习：

- 启动 `turtlesim_node`。
- 写一个控制节点订阅 `/turtle1/pose`。
- 发布 `/turtle1/cmd_vel`。
- 用 P 控制让乌龟朝一个固定目标点运动。

完成标准：

- 能画出节点图。
- 能解释 `/turtle1/pose` 和 `/turtle1/cmd_vel` 的消息方向。
- 能调节 `linear_gain` 和 `angular_gain` 观察效果变化。
- 能说明为什么角速度要根据角度误差闭环控制。

### 第 2 周：工作空间、包和接口

目标：能自己创建 ROS 2 Python 包，并理解包结构。

要学：

- `colcon build`
- `ament_python`
- `package.xml`
- `setup.py`
- 自定义 `msg/srv/action`
- launch 文件

练习：

- 建一个 `robot_bringup` 包。
- 建一个自定义消息包，定义简化版检测结果。
- 用 launch 一次性启动多个节点。

当前进度：

- 第 2 周按 3 节课推进。
- 第 1 节 `ros2 launch` 和 YAML 参数文件已完成并通过实操理解。
- 第 2 节进入 `robot_bringup` 包与工作空间组织，新增独立启动编排包。
- 第 3 节 `robot_interfaces` 自定义接口与综合练习已完成，定义 `TargetDetection.msg` 和 `SetGoal.srv`，并用 `/set_goal` 服务跑通目标点更新。
- 第 2 周已完成，下一步进入第 3 周 tf2、URDF 与 RViz。

### 第 3 周：tf2、URDF 与 RViz

目标：理解机器人系统中的坐标系。

要学：

- `map`
- `odom`
- `base_link`
- `camera_link`
- `laser_link`
- URDF / Xacro
- `robot_state_publisher`
- RViz

练习：

- 建一个差速小车 URDF。
- 添加摄像头和雷达 frame。
- 在 RViz 中检查 TF 树。

### 第 4 周：Gazebo 仿真

目标：在仿真环境里跑机器人，不急着上真机。

要学：

- Gazebo Harmonic
- `ros_gz_bridge`
- `/cmd_vel`
- `/scan`
- `/odom`
- `/camera/image_raw`

练习：

- Gazebo 中生成小车。
- 键盘控制小车运动。
- RViz 同步显示雷达、图像、TF 和里程计。

### 第 5 周：YOLO 接入 ROS 2

目标：把已有 YOLO 能力封装成 ROS 2 节点。

要学：

- `sensor_msgs/Image`
- `cv_bridge`
- `image_transport`
- QoS
- `rosbag2`

练习：

- YOLO 节点订阅相机图像。
- 发布检测框结果。
- 用 rosbag2 录制和回放测试数据。

### 第 6 周：控制理论落地

目标：把控制理论落实到机器人速度控制。

要学：

- 差速小车运动学。
- P / PID 控制。
- 速度限幅。
- 滤波。
- 控制频率。

练习：

- 根据 YOLO 检测框中心控制角速度。
- 根据目标距离控制线速度。
- 加入限幅，避免速度突变。

### 第 7 周：SLAM 与 Nav2

目标：让机器人建图并导航到目标点。

要学：

- SLAM Toolbox。
- AMCL。
- Nav2 planner。
- Nav2 controller。
- costmap。
- behavior tree。

练习：

- 在 Gazebo 中建图。
- 保存地图。
- 用 Nav2 从 A 点导航到 B 点。

### 第 8 周以后：综合项目

项目建议：

> 基于 ROS 2 + YOLO + Nav2 的目标搜索与跟随机器人仿真系统。

模块建议：

- `robot_description`：机器人模型。
- `robot_bringup`：统一启动文件。
- `yolo_detector`：图像检测。
- `target_tracker`：目标选择和滤波。
- `target_controller`：目标跟随控制。
- `navigation_task`：巡航、发现目标、切换跟随。

## 第 1 周学习笔记：turtlesim P 控制

### 系统结构

节点：

- `/turtlesim`：仿真乌龟，发布位姿并订阅速度命令。
- `/turtle_goal_controller`：目标控制节点，订阅位姿，发布速度。

话题：

- `/turtle1/pose`：乌龟当前位姿。
- `/turtle1/cmd_vel`：速度控制命令。

数据流：

```text
/turtlesim --/turtle1/pose--> /turtle_goal_controller
/turtle_goal_controller --/turtle1/cmd_vel--> /turtlesim
```

### 控制思路

目标点设为 `(goal_x, goal_y)`。每次收到当前位姿 `(x, y, theta)` 后：

```text
dx = goal_x - x
dy = goal_y - y
distance_error = sqrt(dx^2 + dy^2)
target_angle = atan2(dy, dx)
angle_error = normalize(target_angle - theta)
```

控制律：

```text
linear.x = linear_gain * distance_error
angular.z = angular_gain * angle_error
```

再加入限幅：

```text
linear.x <= max_linear_speed
abs(angular.z) <= max_angular_speed
```

接近目标时停止：

```text
if distance_error < goal_tolerance:
    linear.x = 0
    angular.z = 0
```

### 为什么这是 P 控制

P 控制的输出与误差成正比。距离误差越大，线速度越大；角度误差越大，角速度越大。这个练习的重点不是得到最优控制效果，而是理解 ROS 2 闭环控制节点的结构。

### 调试命令

```bash
ros2 run turtlesim turtlesim_node
ros2 run turtlesim_p_controller turtle_goal_controller
ros2 launch turtlesim_p_controller turtlesim_goal.launch.py
ros2 topic list
ros2 topic echo /turtle1/pose
ros2 topic echo /turtle1/cmd_vel
ros2 node list
ros2 node info /turtle_goal_controller
rqt_graph
```

## 第 2 周第 1 小课学习笔记：launch 与参数 YAML

新增文件：

- `src/turtlesim_p_controller/launch/turtlesim_goal.launch.py`
- `src/turtlesim_p_controller/config/goal_controller.yaml`
- `src/turtlesim_p_controller/WEEK_02_01_LAUNCH_AND_PARAMS.md`

核心理解：

```text
launch 文件负责一次启动多个节点
YAML 文件负责保存节点默认参数
setup.py 的 data_files 负责把 launch/config 安装到 install/ 目录
```

运行方式：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select turtlesim_p_controller
source install/setup.bash
ros2 launch turtlesim_p_controller turtlesim_goal.launch.py
```

参数检查：

```bash
ros2 param get /turtle_goal_controller goal_x
ros2 param get /turtle_goal_controller angular_gain
```

临时修改目标点：

```bash
ros2 param set /turtle_goal_controller goal_x 2.0
ros2 param set /turtle_goal_controller goal_y 2.0
```

## 第 2 周第 2 小课学习笔记：robot_bringup 与工作空间组织

新增 package：

```text
src/robot_bringup
```

核心理解：

```text
turtlesim_p_controller 是功能包
robot_bringup 是启动编排包
src/ 放源码
build/ 放构建中间文件
install/ 放运行时安装结果
log/ 放构建日志
```

推荐启动入口：

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
colcon build --packages-select turtlesim_p_controller robot_bringup
source install/setup.bash
ros2 launch robot_bringup turtlesim_goal.launch.py
```

检查节点：

```bash
ros2 node list --no-daemon
```

检查 bringup 的 launch 文件是否安装：

```bash
find install/robot_bringup/share/robot_bringup -maxdepth 3 -type f | sort
```

## 第 2 周第 3 小课学习笔记：自定义接口与综合练习

新增 package：

```text
src/robot_interfaces
```

核心理解：

```text
robot_interfaces 是接口包
turtlesim_p_controller 是功能包
robot_bringup 是启动编排包
msg 用于 topic 消息
srv 用于 service 请求和响应
```

构建三个包：

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
colcon build --packages-select robot_interfaces turtlesim_p_controller robot_bringup
source install/setup.bash
```

查看自定义接口：

```bash
ros2 interface show robot_interfaces/msg/TargetDetection
ros2 interface show robot_interfaces/srv/SetGoal
```

模拟发布检测结果：

```bash
ros2 topic pub --once /target_detection robot_interfaces/msg/TargetDetection \
  "{label: 'person', confidence: 0.92, center_x: 0.5, center_y: 0.4, width: 0.2, height: 0.3, is_tracking: true}"
```

用自定义服务修改目标点：

```bash
ros2 launch robot_bringup turtlesim_goal.launch.py
ros2 service list | grep set_goal
ros2 service call /set_goal robot_interfaces/srv/SetGoal "{x: 2.0, y: 8.0}"
```

注意：

```text
ros2 interface show 能看到接口，只说明 robot_interfaces 构建好了。
ros2 service list 能看到 /set_goal，才说明控制器节点真的启动了这个服务。
如果 service call 一直 waiting for service，需要重启 launch。
```

## 每周复盘模板

### 本周完成

- 待填写

### 卡住的问题

- 待填写

### 我真正理解了什么

- 待填写

### 还需要补的知识

- 待填写

### 下周任务

- 待填写
