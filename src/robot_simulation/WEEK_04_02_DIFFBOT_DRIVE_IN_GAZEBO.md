# 第 4 周第 2 小课：让差速小车在 Gazebo 里动起来

## 本课目标

上一课只启动了 Gazebo 空世界，并把 Gazebo `/clock` 桥接到 ROS 2 `/clock`。这一课加入一个最小差速小车，让它真正接收 ROS 2 的速度命令并在 Gazebo 中运动。

完成后你应该能理解：

- Gazebo 里的轮子必须是可转动 joint，不能再用上一周 RViz 模型里的 fixed joint。
- DiffDrive 插件读取速度命令，控制左右轮 joint。
- `/cmd_vel` 的方向是 ROS 2 到 Gazebo。
- `/odom` 的方向是 Gazebo 到 ROS 2。
- Gazebo GUI 中看到的是物理仿真结果，ROS 2 中看到的是 bridge 转换后的话题。

## 本课数据流

```text
ROS 2 /cmd_vel
  -> ros_gz_bridge
  -> Gazebo /cmd_vel
  -> Gazebo DiffDrive plugin
  -> left_wheel_joint / right_wheel_joint
  -> Gazebo /odom
  -> ros_gz_bridge
  -> ROS 2 /odom
```

注意方向：

```text
/cmd_vel: ROS_TO_GZ
/odom:    GZ_TO_ROS
/clock:   GZ_TO_ROS
```

## 为什么这一课先用 SDF 小车

第 3 周的 `robot_description` 模型主要服务 RViz 和 TF 教学，轮子 joint 还是 `fixed`。Gazebo 要让轮子真实转动，需要：

- 轮子 joint 是 `revolute`。
- link 有合理的 collision 和 inertial。
- 模型中加载 Gazebo 的 DiffDrive 系统插件。

所以这一课先在 `robot_simulation/worlds/diffbot_drive.world.sdf` 里直接写一个最小 SDF 小车。这样能把 Gazebo 物理和插件讲清楚，不把 URDF/Xacro 转 Gazebo 的细节混进来。后续再逐步统一模型来源。

## 本课新增文件

```text
src/robot_simulation/
├── config/
│   └── diff_drive_bridge.yaml
├── launch/
│   └── diffbot_drive.launch.py
├── worlds/
│   └── diffbot_drive.world.sdf
└── WEEK_04_02_DIFFBOT_DRIVE_IN_GAZEBO.md
```

## 文件 1：差速小车 world

文件：

```text
src/robot_simulation/worlds/diffbot_drive.world.sdf
```

这个 world 包含：

- 地面和太阳光。
- `diffbot` 模型。
- `base_link` 车体。
- `left_wheel_link` 和 `right_wheel_link` 两个轮子。
- `left_wheel_joint` 和 `right_wheel_joint` 两个 `revolute` joint。
- `front_caster_link` 和 `rear_caster_link` 两个辅助支撑小球。
- `gz::sim::systems::DiffDrive` 插件。

本课采用 ROS 常见坐标约定：`x` 向前，`y` 向左，`z` 向上。左右轮的轮轴横穿车体，方向是左右方向，所以轮子 joint 的旋转轴写成：

```xml
<axis>
  <xyz>0 1 0</xyz>
</axis>
```

这里还要区分两个概念：

- joint 轴：轮子真实绕哪个轴转，本课是 `0 1 0`。
- visual/collision 几何姿态：Gazebo 的 cylinder 默认沿局部 `z` 轴拉长，所以需要在 wheel 的 `visual` 和 `collision` 里写 `<pose>0 0 0 1.5708 0 0</pose>`，把圆柱轴转到 `y` 方向。

不要把 wheel link 自身整体 roll 90 度。link frame 保持和模型坐标对齐，几何圆柱单独旋转，这样 joint 轴、轮子视觉方向和 DiffDrive 插件更容易对应。

还要注意，“轮子让车向前走”和“旋转轴向前”不是一回事。车向 `+x` 前进时，轮轴仍然沿 `y`；轮子绕 `y` 轴转，轮缘在接地点相对轮心向后，车体中心向前，这才是不打滑滚动的关系。也就是说，和前进方向一致的是轮子接地点产生的运动效果，不是旋转轴本身。

如果看到别的 Gazebo 示例使用 `0 0 1`，通常是因为那个示例把轮子 link 的局部坐标系或圆柱几何方向摆成了另一种方式。判断标准不是死记 `z` 或 `y`，而是看轮轴在当前 link/joint 坐标系里沿哪个方向。

前后两个 caster 分别放在 `x=0.16` 和 `x=-0.16`，和左右轮一起形成更大的支撑区域。之前只有后方一个 caster 时，支撑区域前边界接近轮轴，车体和传感器重心容易压在边界附近；Gazebo 中落地或原地转向时可能绕轮轴翘起。这里用前后两个小球支撑，是为了让重心更稳定地落在接地点围成的区域内。

DiffDrive 插件关键配置：

```xml
<plugin filename="gz-sim-diff-drive-system" name="gz::sim::systems::DiffDrive">
  <left_joint>left_wheel_joint</left_joint>
  <right_joint>right_wheel_joint</right_joint>
  <wheel_separation>0.36</wheel_separation>
  <wheel_radius>0.07</wheel_radius>
  <topic>/cmd_vel</topic>
  <odom_topic>/odom</odom_topic>
  <frame_id>odom</frame_id>
  <child_frame_id>base_link</child_frame_id>
</plugin>
```

这里的参数含义：

- `left_joint` / `right_joint`：插件要控制的左右轮 joint 名称。
- `wheel_separation`：左右轮中心距离。
- `wheel_radius`：轮子半径。
- `topic`：Gazebo 侧接收速度命令的话题。
- `odom_topic`：Gazebo 侧发布里程计的话题。
- `frame_id`：里程计父坐标系。
- `child_frame_id`：机器人本体坐标系。

## 文件 2：DiffDrive bridge 配置

文件：

```text
src/robot_simulation/config/diff_drive_bridge.yaml
```

这一课桥接 3 个话题：

```yaml
- ros_topic_name: "/clock"
  gz_topic_name: "/clock"
  ros_type_name: "rosgraph_msgs/msg/Clock"
  gz_type_name: "gz.msgs.Clock"
  direction: GZ_TO_ROS

- ros_topic_name: "/cmd_vel"
  gz_topic_name: "/cmd_vel"
  ros_type_name: "geometry_msgs/msg/Twist"
  gz_type_name: "gz.msgs.Twist"
  direction: ROS_TO_GZ

- ros_topic_name: "/odom"
  gz_topic_name: "/odom"
  ros_type_name: "nav_msgs/msg/Odometry"
  gz_type_name: "gz.msgs.Odometry"
  direction: GZ_TO_ROS
```

最重要的是方向：

- `/cmd_vel` 是控制命令，从 ROS 2 发给 Gazebo。
- `/odom` 是仿真结果，从 Gazebo 发回 ROS 2。

## 文件 3：启动入口

文件：

```text
src/robot_simulation/launch/diffbot_drive.launch.py
```

它做两件事：

- 用 `ros_gz_sim` 启动 `diffbot_drive.world.sdf`。
- 用 `ros_gz_bridge` 加载 `diff_drive_bridge.yaml`。

## 运行步骤

构建：

```bash
cd ~/ros
source /opt/ros/jazzy/setup.bash
colcon build --packages-select robot_simulation
source install/setup.bash
```

启动 Gazebo 小车：

```bash
ros2 launch robot_simulation diffbot_drive.launch.py
```

另开终端，确认 ROS 2 侧有话题：

```bash
cd ~/ros
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 topic list | grep -E "/cmd_vel|/odom|/clock"
```

发送前进命令：

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.25}, angular: {z: 0.0}}"
```

发送左转命令：

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.7}}"
```

停止：

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

查看里程计：

```bash
ros2 topic echo /odom --once
```

## 观察问题

1. 发布 `/cmd_vel` 后，Gazebo 里的小车是否移动？
2. `/odom` 的 `pose.pose.position.x` 是否随着前进命令变化？
3. `/cmd_vel` 和 `/odom` 的 bridge 方向为什么相反？
4. 为什么第 3 周的轮子 fixed joint 不能直接用于这一课的真实轮子运动？

## 常见问题

### 1. 小车不动

先确认 bridge 节点是否存在：

```bash
ros2 node list | grep diff_drive_bridge
```

再确认 `/cmd_vel` 是否有订阅者：

```bash
ros2 topic info /cmd_vel --verbose
```

如果没有 Gazebo 侧订阅者，优先检查 `diff_drive_bridge.yaml` 是否被 launch 加载。

### 2. `/odom` 没有输出

先确认 Gazebo 仍在运行，然后看 Gazebo 侧 topic：

```bash
gz topic -l | grep odom
```

如果 Gazebo 侧没有 `/odom`，检查 DiffDrive 插件是否加载，以及 world 里的 `odom_topic` 是否写成 `/odom`。

### 3. 小车方向和预期相反

差速车方向由轮子 joint 轴和左右轮配置共同决定。如果后续发现前进命令导致小车后退，需要检查：

- 左右轮 joint 是否接反。
- wheel joint 的 `<axis><xyz>...</xyz></axis>` 是否和轮子几何方向一致。
- `left_joint`、`right_joint` 是否对应正确。

这一课先以能闭环控制和读到 odom 为完成标准。

## 练习

### 练习 1：前进 1 秒再停止

终端 1 启动：

```bash
ros2 launch robot_simulation diffbot_drive.launch.py
```

终端 2 发送：

```bash
ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.25}, angular: {z: 0.0}}"
```

保持 1 秒后按 `Ctrl-C`，再发送停止命令：

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

### 练习 2：查看 odom

运行：

```bash
ros2 topic echo /odom --once
```

观察：

- `header.frame_id` 是否是 `odom`。
- `child_frame_id` 是否是 `base_link`。
- `pose.pose.position` 是否有变化。

### 练习 3：理解方向

画出下面的数据流：

```text
ROS 2 /cmd_vel -> Gazebo /cmd_vel -> DiffDrive -> Gazebo /odom -> ROS 2 /odom
```

并标出哪一段是 `ROS_TO_GZ`，哪一段是 `GZ_TO_ROS`。

## 知识问答

问题 1：

```text
DiffDrive 插件直接订阅 ROS 2 的 /cmd_vel 吗？
```

参考答案：

```text
不是。DiffDrive 插件在 Gazebo 内部订阅 Gazebo Transport 的 /cmd_vel。ROS 2 的 /cmd_vel 需要先通过 ros_gz_bridge 转成 Gazebo 消息。
```

问题 2：

```text
为什么 /odom 是 GZ_TO_ROS？
```

参考答案：

```text
里程计是 Gazebo 根据仿真物理和轮子运动计算出来的结果。ROS 2 节点需要读取这个结果，所以方向是 Gazebo 到 ROS。
```

问题 3：

```text
为什么轮子 joint 要用 revolute？
```

参考答案：

```text
轮子需要绕轴连续旋转。fixed joint 不允许相对运动，DiffDrive 插件无法驱动 fixed joint 产生真实轮子转动。
```

问题 4：

```text
这一课为什么还不接 RViz？
```

参考答案：

```text
这一课只验证运动闭环：cmd_vel 能让 Gazebo 小车动起来，并且 odom 能回到 ROS 2。RViz、LaserScan 和相机图像会在下一课一起接入，避免一次引入太多链路。
```

## 完成标准

完成本课后，你应该能做到：

- 启动 `diffbot_drive.launch.py`，在 Gazebo 中看到小车。
- 发布 `/cmd_vel` 后，小车能前进或转向。
- 运行 `ros2 topic echo /odom --once` 能看到里程计。
- 能解释 `/cmd_vel` 和 `/odom` 的 bridge 方向。
- 能说明为什么 Gazebo 中的轮子需要 `revolute` joint。

下一课会把雷达、相机、TF 和 RViz 同步接起来。
