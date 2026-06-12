# 第 4 周第 1 小课：Gazebo Harmonic 与 ros_gz 最小链路

## 本课目标

这一课先不放入小车，也不急着接雷达和相机。目标是把 Gazebo 和 ROS 2 之间的最小链路跑通：

- 确认当前环境是否已经安装 Gazebo Harmonic 和 `ros_gz`。
- 理解 Gazebo topic 和 ROS topic 是两个不同通信系统。
- 用 `ros_gz_bridge` 把 Gazebo 的 `/clock` 转成 ROS 2 的 `/clock`。
- 从 ROS 2 launch 文件启动一个 Gazebo 空世界。

## 为什么第 4 周先做环境和桥接

前三周我们一直在 ROS 2 内部工作：

```text
URDF/Xacro -> robot_state_publisher -> /robot_description + /tf_static -> RViz
```

Gazebo 加进来以后，系统会变成两个通信域：

```text
Gazebo Sim / Gazebo Transport  <->  ros_gz_bridge  <->  ROS 2 graph
```

Gazebo 负责物理仿真、碰撞、传感器和仿真时间。ROS 2 负责节点编排、控制算法、RViz、Nav2 和后续 YOLO 节点。两边的话题名字可以相同，但消息系统不是同一个，所以需要 bridge。

## 推荐版本

当前学习环境继续使用：

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic

Gazebo 官方文档把 ROS 2 Jazzy + Gazebo Harmonic 标为推荐组合。新手优先从 ROS 仓库安装默认匹配包：

```bash
sudo apt update
sudo apt install ros-jazzy-ros-gz
```

参考资料：

- Gazebo ROS 安装说明：<https://gazebosim.org/docs/harmonic/ros_installation/>
- 从 ROS 2 launch 启动 Gazebo：<https://gazebosim.org/docs/harmonic/ros2_launch_gazebo/>
- `ros_gz_bridge` 配置说明：<https://github.com/gazebosim/ros_gz/tree/ros2/ros_gz_bridge>

## 先检查本机是否已安装

每次打开新终端，先进入工作空间并加载 ROS 2：

```bash
cd ~/ros
source /opt/ros/jazzy/setup.bash
```

检查 Gazebo 命令：

```bash
command -v gz
```

如果没有输出，说明 `gz` 命令还没安装到当前环境。

检查 ROS-Gazebo 包：

```bash
ros2 pkg prefix ros_gz_sim
ros2 pkg prefix ros_gz_bridge
```

如果输出类似：

```text
Package not found
```

说明需要先安装：

```bash
sudo apt update
sudo apt install ros-jazzy-ros-gz
```

安装后重新开终端，或者重新加载环境：

```bash
source /opt/ros/jazzy/setup.bash
```

## 本课新增包

本课新增：

```text
src/robot_simulation/
```

它只负责 Gazebo 仿真相关资产：

```text
robot_simulation/
├── config/
│   └── clock_bridge.yaml
├── launch/
│   └── gazebo_empty_world.launch.py
├── worlds/
│   └── empty_diffbot.world.sdf
├── package.xml
└── setup.py
```

职责划分保持不变：

- `robot_description`：机器人几何模型、URDF/Xacro、RViz 模型显示。
- `robot_simulation`：Gazebo world、bridge 配置和仿真启动入口。
- `robot_bringup`：后续负责把模型、仿真、RViz、控制统一编排起来。

## 文件 1：空 Gazebo world

文件：

```text
src/robot_simulation/worlds/empty_diffbot.world.sdf
```

这个 world 只有三类东西：

- Gazebo 系统插件：物理、用户命令、场景广播。
- 光源：让 GUI 中能看到地面。
- 地面：后续让小车可以落在平面上。

这一课不把机器人放进去，是为了先确认 Gazebo 本身和 `/clock` bridge 正常。

## 文件 2：clock bridge 配置

文件：

```text
src/robot_simulation/config/clock_bridge.yaml
```

内容核心是：

```yaml
- ros_topic_name: "/clock"
  gz_topic_name: "/clock"
  ros_type_name: "rosgraph_msgs/msg/Clock"
  gz_type_name: "gz.msgs.Clock"
  direction: GZ_TO_ROS
  qos_profile: CLOCK
```

这里的方向是 `GZ_TO_ROS`，意思是：

```text
Gazebo /clock -> ROS 2 /clock
```

仿真时间只能由仿真器产生，ROS 节点消费这个时间。不要反过来让 ROS 给 Gazebo 发布时间。

## 文件 3：Gazebo 启动入口

文件：

```text
src/robot_simulation/launch/gazebo_empty_world.launch.py
```

这个 launch 做两件事：

- include `ros_gz_sim` 提供的 `gz_sim.launch.py`，打开 Gazebo GUI 和 server。
- 启动 `ros_gz_bridge` 的 `parameter_bridge`，加载 `clock_bridge.yaml`。

数据流是：

```text
empty_diffbot.world.sdf -> Gazebo Sim
Gazebo /clock -> ros_gz_bridge -> ROS 2 /clock
```

## 运行步骤

构建本课包：

```bash
cd ~/ros
source /opt/ros/jazzy/setup.bash
colcon build --packages-select robot_simulation
source install/setup.bash
```

启动 Gazebo 空世界：

```bash
ros2 launch robot_simulation gazebo_empty_world.launch.py
```

如果 Gazebo 窗口打开，并能看到灰色地面，第一步成功。

另开一个终端，检查 ROS 2 是否收到仿真时间：

```bash
cd ~/ros
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 topic list | grep clock
ros2 topic echo /clock --once
```

如果能看到 `/clock`，并且 `ros2 topic echo /clock --once` 输出了时间戳，说明最小 bridge 成功。

再看 Gazebo 自己的话题：

```bash
gz topic -l
```

你会看到 Gazebo Transport 里的话题。注意：`gz topic -l` 看到的是 Gazebo 的通信域，`ros2 topic list` 看到的是 ROS 2 的通信域。

## 常见问题

### 1. `Package 'ros_gz_sim' not found`

原因：没有安装 `ros-jazzy-ros-gz`，或者当前终端没有 `source /opt/ros/jazzy/setup.bash`。

处理：

```bash
source /opt/ros/jazzy/setup.bash
ros2 pkg prefix ros_gz_sim
```

如果仍然找不到：

```bash
sudo apt update
sudo apt install ros-jazzy-ros-gz
```

### 2. `command -v gz` 没有输出

原因：Gazebo CLI 没安装到当前系统。

处理方式同上，优先安装 `ros-jazzy-ros-gz`。

### 3. `/clock` 没有输出

先确认 Gazebo launch 是否还在运行，再检查 bridge 节点：

```bash
ros2 node list
ros2 topic list | grep clock
```

如果 Gazebo 已退出，`/clock` 也不会继续更新。

## 观察问题

1. `ros2 topic list` 和 `gz topic -l` 的输出是否完全相同？
2. `/clock` 是 Gazebo 到 ROS，还是 ROS 到 Gazebo？
3. 为什么这一课先不放机器人？
4. `robot_simulation` 和 `robot_description` 的职责有什么区别？

## 练习

### 练习 1：环境诊断

运行：

```bash
command -v gz
ros2 pkg prefix ros_gz_sim
ros2 pkg prefix ros_gz_bridge
```

把输出记录下来，并判断当前环境是否已具备 Gazebo 仿真条件。

### 练习 2：启动空世界

运行：

```bash
colcon build --packages-select robot_simulation
source install/setup.bash
ros2 launch robot_simulation gazebo_empty_world.launch.py
```

观察 Gazebo GUI 是否打开，是否能看到地面。

### 练习 3：检查 `/clock`

在第二个终端运行：

```bash
ros2 topic echo /clock --once
```

确认 ROS 2 能收到 Gazebo 的仿真时间。

## 知识问答

问题 1：

```text
Gazebo topic 和 ROS topic 是同一个东西吗？
```

参考答案：

```text
不是。Gazebo 使用 Gazebo Transport，ROS 2 使用 DDS/ROS graph。二者可以有相同的话题名，但消息系统不同，需要 ros_gz_bridge 转换。
```

问题 2：

```text
为什么 /clock bridge 要用 GZ_TO_ROS？
```

参考答案：

```text
仿真时间由 Gazebo 产生。ROS 2 节点需要消费仿真时间，所以方向应该是 Gazebo 到 ROS，而不是 ROS 到 Gazebo。
```

问题 3：

```text
robot_simulation 包应该保存 URDF/Xacro 吗？
```

参考答案：

```text
不建议。URDF/Xacro 描述机器人模型，继续归 robot_description。robot_simulation 只保存 Gazebo world、bridge 配置和仿真 launch，避免职责混在一起。
```

问题 4：

```text
如果 ros2 topic list 看不到 /clock，应该先查什么？
```

参考答案：

```text
先确认 Gazebo launch 还在运行，再检查 ros_gz_bridge 节点是否启动，以及 clock_bridge.yaml 是否被加载。
```

## 完成标准

完成本课后，你应该能做到：

- 说出当前环境是否安装了 Gazebo 和 `ros_gz`。
- 知道 `ros-jazzy-ros-gz` 是 Jazzy 下推荐的 Gazebo/ROS 桥接安装入口。
- 能启动 `robot_simulation` 的 Gazebo 空世界。
- 能通过 `/clock` 解释 Gazebo 到 ROS 2 的最小 bridge。
- 能区分 `robot_description` 和 `robot_simulation` 的职责。

下一课再把差速小车模型放进 Gazebo，并让 `/cmd_vel` 真正驱动小车运动。
