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
- 第 2 周已完成。

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

当前进度：

- 第 3 周第 1 小课已完成，新增 `tf2_frame_demo` 示例包。
- 第 1 小课先不进入 URDF，先用 `map -> odom -> base_link -> camera_link` 这棵最小 TF 树理解坐标关系。
- `map -> odom` 和 `base_link -> camera_link` 是静态 transform。
- `odom -> base_link` 是动态 transform，由 `dynamic_frame_broadcaster` 周期发布。
- `frame_listener` 查询 `map -> camera_link`，用于观察 tf2 如何沿 TF 树推导间接坐标关系。
- 第 1 小课已加入 RViz2 可视化观察：设置 `Fixed Frame = map`，添加 `TF` display，观察 `base_link` 绕 `odom` 运动、`camera_link` 跟随 `base_link`。
- 第 3 周第 2 小课开始，新增 `robot_description` 包。
- 第 2 小课创建 `urdf/diffbot.urdf`，用 URDF 描述简化差速小车的 `base_link`、左右轮、摄像头和雷达 frame。
- 第 2 小课的正式 RViz2 配置保存为 `src/robot_description/rviz/display.rviz`。
- 当前环境没有安装 `joint_state_publisher` / `joint_state_publisher_gui`，所以本课先把轮子、摄像头和雷达都作为 fixed joint 观察，后续 Gazebo 和控制课再引入轮子真实旋转和 `/joint_states`。
- 第 3 周第 3 小课开始，新增 `diffbot.urdf.xacro`、`diffbot_materials.xacro` 和 `diffbot_components.xacro`。
- 第 3 小课把模型尺寸、颜色和重复组件拆成 Xacro property/macro/include，并新增 `robot_bringup/launch/display_robot.launch.py` 作为推荐模型显示入口。

第 3 周第 1 小课运行：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select tf2_frame_demo
source install/setup.bash
ros2 launch tf2_frame_demo tf2_demo.launch.py
```

查看 TF：

```bash
ros2 run tf2_ros tf2_echo map camera_link
rviz2
ros2 run tf2_tools view_frames
```

第 3 周第 2/3 小课运行：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select robot_description robot_bringup
source install/setup.bash
ros2 launch robot_bringup display_robot.launch.py
```

直接启动模型包入口也可以：

```bash
ros2 launch robot_description display.launch.py
```

检查 Xacro 展开：

```bash
xacro src/robot_description/urdf/diffbot.urdf.xacro
```

查看模型 frame：

```bash
ros2 run tf2_ros tf2_echo base_link camera_link
ros2 run tf2_ros tf2_echo base_link laser_link
ros2 run tf2_tools view_frames
```

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

当前进度：

- 第 4 周第 1 小课开始，新增 `robot_simulation` 包。
- 本课先不放入小车，先验证 Gazebo Harmonic、`ros_gz_sim` 和 `ros_gz_bridge` 环境。
- 新增 `worlds/empty_diffbot.world.sdf`，作为后续仿真的空世界。
- 新增 `config/clock_bridge.yaml`，把 Gazebo `/clock` 单向桥接到 ROS 2 `/clock`。
- 新增 `launch/gazebo_empty_world.launch.py`，从 ROS 2 launch 启动 Gazebo 空世界和 clock bridge。

第 4 周第 1 小课运行：

```bash
source /opt/ros/jazzy/setup.bash
command -v gz
ros2 pkg prefix ros_gz_sim
ros2 pkg prefix ros_gz_bridge
```

如果找不到 Gazebo/ros_gz：

```bash
sudo apt update
sudo apt install ros-jazzy-ros-gz
```

启动空世界：

```bash
colcon build --packages-select robot_simulation
source install/setup.bash
ros2 launch robot_simulation gazebo_empty_world.launch.py
```

检查 `/clock`：

```bash
ros2 topic echo /clock --once
gz topic -l
```

第 4 周第 2 小课开始，新增可运动差速小车仿真：

- 新增 `worlds/diffbot_drive.world.sdf`，直接在 Gazebo SDF world 中定义最小可动 `diffbot`。
- 左右轮 joint 改为 `revolute`，并由 Gazebo `DiffDrive` 插件控制。
- 新增 `config/diff_drive_bridge.yaml`，桥接 `/clock`、`/cmd_vel` 和 `/odom`。
- 新增 `launch/diffbot_drive.launch.py`，启动可运动小车 world 和 bridge。
- 本课只验证 `/cmd_vel` 控制与 `/odom` 回传，雷达、相机和 RViz 放到下一课。
- 第 4 周第 3 小课加入键盘控制、雷达、相机、TF 和 RViz 同步显示。
- 新增 `worlds/diffbot_sensors.world.sdf`，在 Gazebo 小车上挂载 `front_lidar` 和 `front_camera`，并加入障碍物用于观察。
- 新增 `config/sensor_bridge.yaml`，桥接 `/clock`、`/cmd_vel`、`/odom`、`/scan`、`/camera/image_raw` 和 `/camera/camera_info`。
- 新增 `robot_simulation/odom_to_tf.py`，把 `/odom` 转成 `odom -> base_link` 动态 TF。
- 新增 `rviz/sensors.rviz`，在 RViz 中同步显示 RobotModel、TF、LaserScan 和相机图像。
- 本课键盘控制直接运行 `teleop_twist_keyboard`，不要通过 `ros2 launch` 后台启动，因为它需要读取真实交互终端的键盘输入。
- Gazebo 小车使用前后两个 caster 小球辅助支撑；单后 caster 虽然看起来也有支撑，但原地转向时支撑区域太小，容易绕轮轴翘起。RViz 正常只说明显示链路正常，不代表 Gazebo 物理稳定。

第 4 周第 2 小课运行：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select robot_simulation
source install/setup.bash
ros2 launch robot_simulation diffbot_drive.launch.py
```

另开终端发送速度命令：

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.25}, angular: {z: 0.0}}"
ros2 topic echo /odom --once
```

第 4 周第 3 小课运行：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select robot_description robot_simulation
source install/setup.bash
ros2 launch robot_simulation diffbot_sensors_rviz.launch.py
```

另开终端启动键盘控制：

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

常用按键：

```text
i 前进，, 后退，j 左转，l 右转，k 停止。
```

本课要重点理解：

- 键盘节点只发布 ROS 2 `/cmd_vel`，Gazebo 轮子仍由 DiffDrive 插件控制。
- `/odom` 是消息，RViz 需要 TF，所以要用 `odom_to_tf` 发布 `odom -> base_link`。
- `robot_state_publisher` 负责固定 TF，例如 `base_link -> laser_link` 和 `camera_link -> camera_optical_frame`。
- 传感器消息的 `header.frame_id` 必须和 TF 树里的 frame 对齐，否则 RViz 无法知道数据在空间中的位置。

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

## 第 3 周第 1 小课学习笔记：tf2 与坐标系入门

新增 package：

```text
src/tf2_frame_demo
```

核心理解：

```text
frame 是一个坐标系
transform 是两个 frame 之间的位置和姿态关系
TF 树把多个 transform 串起来
tf2 可以沿 TF 树推导间接坐标关系
```

本课 TF 树：

```text
map
└── odom
    └── base_link
        └── camera_link
```

其中：

```text
map -> odom 是静态 transform
odom -> base_link 是动态 transform
base_link -> camera_link 是静态 transform
```

运行：

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
colcon build --packages-select tf2_frame_demo
source install/setup.bash
ros2 launch tf2_frame_demo tf2_demo.launch.py
```

查看 TF：

```bash
ros2 run tf2_ros tf2_echo map camera_link
ros2 run tf2_tools view_frames
rviz2
```

RViz2 观察重点：

```text
Fixed Frame 设置为 map
添加 TF display
观察 base_link 绕 odom 运动
观察 camera_link 跟随 base_link
```

关键区别：

```text
上一阶段 turtlesim 的 /pose 是单个对象的位置消息
tf2 关注的是多个坐标系之间的关系
机器人系统中传感器、底盘、地图、里程计都要靠 TF 对齐
```

## 第 3 周第 2 小课学习笔记：robot_description 与 URDF

新增 package：

```text
src/robot_description
```

新增核心文件：

```text
src/robot_description/urdf/diffbot.urdf
src/robot_description/launch/display.launch.py
src/robot_description/rviz/display.rviz
src/robot_description/WEEK_03_02_ROBOT_DESCRIPTION_URDF.md
```

核心理解：

```text
URDF 描述机器人由哪些 link 组成
joint 描述父 link 和子 link 的连接关系
robot_state_publisher 根据 URDF 发布 TF
RViz2 的 RobotModel 根据 /robot_description 显示模型
```

本课模型：

```text
base_link
├── left_wheel_link
├── right_wheel_link
├── camera_link
│   └── camera_optical_frame
└── laser_link
```

运行：

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
colcon build --packages-select robot_description
source install/setup.bash
ros2 launch robot_description display.launch.py
```

检查模型 frame：

```bash
ros2 run tf2_ros tf2_echo base_link camera_link
ros2 run tf2_ros tf2_echo base_link laser_link
ros2 run tf2_ros tf2_echo camera_link camera_optical_frame
ros2 run tf2_tools view_frames
```

本课暂时全部使用 fixed joint：

```text
fixed joint 不需要 /joint_states
适合先学习传感器和轮子 frame 的安装关系
轮子真实旋转后续 Gazebo 和控制课程再引入
```

`camera_optical_frame` 的意义：

```text
普通机器人坐标系通常是 x 前、y 左、z 上
相机光学坐标系通常是 z 前、x 右、y 下
camera_optical_frame 用来提前适配图像算法和相机消息约定
```

## 第 3 周第 3 小课学习笔记：Xacro 与可复用 bringup

新增核心文件：

```text
src/robot_description/urdf/diffbot.urdf.xacro
src/robot_description/urdf/diffbot_materials.xacro
src/robot_description/urdf/diffbot_components.xacro
src/robot_description/WEEK_03_03_XACRO_AND_BRINGUP.md
src/robot_bringup/launch/display_robot.launch.py
```

核心理解：

```text
Xacro 是生成 URDF 的模板语言
Xacro 展开后仍然是普通 URDF
robot_state_publisher 最终接收的仍然是 robot_description 字符串
```

上一课链路：

```text
diffbot.urdf -> robot_state_publisher -> /robot_description + /tf_static -> RViz
```

本课链路：

```text
diffbot.urdf.xacro -> xacro 展开成 URDF -> robot_state_publisher -> /robot_description + /tf_static -> RViz
```

三个 Xacro 概念：

```text
xacro:property：给尺寸、质量、安装位置命名
xacro:macro：把重复结构做成模板
xacro:include：把模型拆成多个文件复用
```

本课文件职责：

```text
diffbot.urdf.xacro 是顶层模型入口
diffbot_materials.xacro 集中定义颜色材质
diffbot_components.xacro 集中定义轮子、摄像头、雷达组件宏
```

推荐运行：

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
colcon build --packages-select robot_description robot_bringup
source install/setup.bash
ros2 launch robot_bringup display_robot.launch.py
```

直接运行模型包入口也可以：

```bash
ros2 launch robot_description display.launch.py
```

检查 Xacro 展开：

```bash
xacro src/robot_description/urdf/diffbot.urdf.xacro
```

检查 TF：

```bash
ros2 topic echo /tf_static --once
ros2 run tf2_ros tf2_echo base_link camera_link
ros2 run tf2_ros tf2_echo base_link laser_link
```

本课和上一课的区别：

```text
RViz 里看到的模型基本一样
区别在于模型文件更可维护、更可复用
尺寸参数不再散落在 XML 中
左右轮等重复结构由 macro 生成
系统推荐从 robot_bringup 统一启动
```

本课实操确认：

```text
xacro 能展开 diffbot.urdf.xacro
/robot_state_publisher 正常启动
/robot_description 存在
/tf_static 中能看到 base_link 到 camera_link、laser_link、left_wheel_link、right_wheel_link 的固定 transform
RViz2 的 RobotModel 和 TF display 可以观察同一套模型
```

注意：

```text
当前 Jazzy 的 xacro 命令不支持 xacro --version
验证 Xacro 是否安装，用 ros2 pkg prefix xacro
如果 RViz 显示 No tf data，先查 ros2 node list、/tf_static 和 robot_state_publisher 是否存在
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
