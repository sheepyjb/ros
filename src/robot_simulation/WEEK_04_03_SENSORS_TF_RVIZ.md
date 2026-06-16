# 第 4 周第 3 小课：雷达、相机、TF/RViz 同步显示

## 本课目标

上一课已经让差速小车接收 `/cmd_vel` 并发布 `/odom`。这一课把主操作方式改成键盘遥控，并把 Gazebo 中的雷达、相机、里程计和 RViz 显示接成一条完整链路。

完成后你应该能理解：

- `teleop_twist_keyboard` 如何发布 `/cmd_vel` 控制 Gazebo 小车。
- Gazebo 传感器如何通过 `ros_gz_bridge` 变成 ROS 2 的 `/scan`、`/camera/image_raw` 和 `/camera/camera_info`。
- `/odom` 只是消息，不会自动出现在 TF 树中，需要 `odom_to_tf` 转成 `odom -> base_link`。
- `robot_state_publisher` 继续发布 `base_link -> laser_link/camera_link/camera_optical_frame` 等固定 TF。
- RViz 需要同时拿到 RobotModel、TF、LaserScan 和 Image，才能同步观察机器人状态。

## 本课数据流

```text
teleop_twist_keyboard
  -> ROS 2 /cmd_vel
  -> ros_gz_bridge
  -> Gazebo /cmd_vel
  -> Gazebo DiffDrive
  -> Gazebo /odom
  -> ros_gz_bridge
  -> ROS 2 /odom
  -> odom_to_tf
  -> ROS 2 /tf: odom -> base_link
```

传感器链路：

```text
Gazebo front_lidar
  -> Gazebo /scan
  -> ros_gz_bridge
  -> ROS 2 /scan
  -> RViz LaserScan

Gazebo front_camera
  -> Gazebo /camera/image_raw + /camera/camera_info
  -> ros_gz_bridge
  -> ROS 2 /camera/image_raw + /camera/camera_info
  -> RViz Image
```

TF 链路：

```text
odom_to_tf:
  odom -> base_link

robot_state_publisher:
  base_link -> left_wheel_link
  base_link -> right_wheel_link
  base_link -> laser_link
  base_link -> camera_link
  camera_link -> camera_optical_frame
```

## 本课新增文件

```text
src/robot_simulation/
├── config/
│   └── sensor_bridge.yaml
├── launch/
│   └── diffbot_sensors_rviz.launch.py
├── robot_simulation/
│   └── odom_to_tf.py
├── rviz/
│   └── sensors.rviz
├── worlds/
│   └── diffbot_sensors.world.sdf
└── WEEK_04_03_SENSORS_TF_RVIZ.md
```

## 文件 1：带传感器的 Gazebo world

文件：

```text
src/robot_simulation/worlds/diffbot_sensors.world.sdf
```

它在上一课小车基础上新增：

- `gz-sim-sensors-system`，让 Gazebo 发布相机和雷达传感器数据。
- `front_caster_link` 和 `rear_caster_link`，让小车在 Gazebo 里由前后两个小球辅助支撑。
- `laser_link`，带 `front_lidar` 传感器，发布 Gazebo `/scan`。
- `camera_link`，带 `front_camera` 传感器，发布 Gazebo `/camera/image_raw` 和 `/camera/camera_info`。
- `front_box` 和 `left_cylinder` 两个静态障碍物，方便雷达和相机马上看到目标。

注意：RViz 里看到小车模型正常，不代表 Gazebo 物理一定稳定。RViz 显示的是 TF 和可视化模型；Gazebo 还会计算 collision、inertial、接地点和力矩。本课 world 使用前后两个 caster，是为了避免传感器加到车体后，单后 caster 支撑时原地转向容易绕轮轴翘起。

雷达关键配置：

```xml
<sensor name="front_lidar" type="gpu_lidar">
  <topic>/scan</topic>
  <update_rate>10</update_rate>
  <lidar>
    <scan>
      <horizontal>
        <samples>360</samples>
        <min_angle>-1.5708</min_angle>
        <max_angle>1.5708</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.08</min>
      <max>8.0</max>
    </range>
  </lidar>
</sensor>
```

相机关键配置：

```xml
<sensor name="front_camera" type="camera">
  <topic>/camera/image_raw</topic>
  <update_rate>15</update_rate>
  <camera>
    <camera_info_topic>/camera/camera_info</camera_info_topic>
    <horizontal_fov>1.047</horizontal_fov>
    <image>
      <width>320</width>
      <height>240</height>
    </image>
    <optical_frame_id>camera_optical_frame</optical_frame_id>
  </camera>
</sensor>
```

## 文件 2：传感器 bridge 配置

文件：

```text
src/robot_simulation/config/sensor_bridge.yaml
```

这一课 bridge 6 个话题：

```text
/clock              GZ_TO_ROS
/cmd_vel            ROS_TO_GZ
/odom               GZ_TO_ROS
/scan               GZ_TO_ROS
/camera/image_raw   GZ_TO_ROS
/camera/camera_info GZ_TO_ROS
```

其中 `/scan`、`/camera/image_raw` 和 `/camera/camera_info` 使用 `SENSOR_DATA` QoS，并通过 bridge 配置写入 frame：

```yaml
frame_id: "laser_link"
frame_id: "camera_optical_frame"
```

这样 RViz 收到传感器消息时，可以沿 TF 树找到它们相对于 `odom` 的位置。

## 文件 3：odom_to_tf 节点

文件：

```text
src/robot_simulation/robot_simulation/odom_to_tf.py
```

Gazebo bridge 回来的 `/odom` 是 `nav_msgs/msg/Odometry` 消息。RViz 的 TF display、LaserScan display 和 RobotModel display 需要的是 TF 树，所以本课新增一个很小的节点：

```text
订阅 /odom
读取 header.frame_id = odom
读取 child_frame_id = base_link
读取 pose.pose
发布 /tf: odom -> base_link
```

这一步把“里程计消息”变成“坐标变换”。

## 文件 4：RViz 配置

文件：

```text
src/robot_simulation/rviz/sensors.rviz
```

默认显示：

- Grid
- RobotModel
- TF
- LaserScan `/scan`
- Image `/camera/image_raw`

`Fixed Frame` 设置为：

```text
odom
```

原因是小车在 Gazebo 中运动时，`base_link` 会相对 `odom` 变化；以 `odom` 为固定坐标系，RViz 能看到机器人和传感器数据一起移动。

## 文件 5：启动入口

主入口：

```text
src/robot_simulation/launch/diffbot_sensors_rviz.launch.py
```

它启动：

- Gazebo `diffbot_sensors.world.sdf`
- `ros_gz_bridge` + `sensor_bridge.yaml`
- `robot_state_publisher`
- `odom_to_tf`
- RViz2 + `sensors.rviz`

键盘控制不写成 launch 文件。`teleop_twist_keyboard` 需要直接读取终端标准输入，用 `ros2 launch` 启动时子进程拿不到真正的交互 stdin，容易报 `termios.error: Inappropriate ioctl for device`。

所以本课的键盘控制固定在第二个真正的交互终端中直接运行：

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

## 运行步骤

构建：

```bash
cd ~/ros
source /opt/ros/jazzy/setup.bash
colcon build --packages-select robot_description robot_simulation
source install/setup.bash
```

终端 1：启动 Gazebo、bridge、TF 和 RViz：

```bash
ros2 launch robot_simulation diffbot_sensors_rviz.launch.py
```

终端 2：启动键盘控制：

```bash
cd ~/ros
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

常用按键：

```text
i      前进
,      后退
j      左转
l      右转
k      停止
u/o    前进并转向
m/.    后退并转向
q/z    同时增大/减小线速度和角速度
w/x    只增大/减小线速度
e/c    只增大/减小角速度
Ctrl-C 退出
```

## 检查命令

检查 topic：

```bash
ros2 topic list | grep -E "/cmd_vel|/odom|/scan|/camera/image_raw|/camera/camera_info|/tf"
```

检查雷达：

```bash
ros2 topic echo /scan --once
```

重点看：

```text
header.frame_id: laser_link
ranges: [...]
```

检查相机：

```bash
ros2 topic echo /camera/camera_info --once
```

重点看：

```text
header.frame_id: camera_optical_frame
height: 240
width: 320
```

检查 TF：

```bash
ros2 run tf2_ros tf2_echo odom base_link
ros2 run tf2_ros tf2_echo base_link laser_link
ros2 run tf2_ros tf2_echo base_link camera_optical_frame
```

## 观察问题

1. 按 `i` 后，Gazebo 里的小车是否前进？
2. 小车运动时，RViz 里的 RobotModel 是否跟着移动？
3. RViz 里的 LaserScan 点云是否跟随 `laser_link` 移动？
4. 相机图像里是否能看到前方障碍物？
5. 如果关闭 `odom_to_tf`，RViz 为什么还能收到 `/odom`，但无法稳定显示运动中的 RobotModel 和传感器？

## 常见问题

### 1. 键盘按了没反应

先确认光标焦点在运行下面命令的终端里。这个节点读取终端键盘输入，不读取 Gazebo 或 RViz 窗口里的按键。

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

不要用 `ros2 launch` 后台启动这个键盘节点；它需要真正的交互式 stdin。

### 2. RViz 中 LaserScan 报 TF 错误

先查雷达消息的 frame：

```bash
ros2 topic echo /scan --once | grep frame_id
```

再查 TF：

```bash
ros2 run tf2_ros tf2_echo base_link laser_link
```

如果 `/scan` 的 frame 不是 `laser_link`，检查 `sensor_bridge.yaml` 里的 `frame_id`。

### 3. RViz 中 RobotModel 不跟着动

先确认 `/tf` 有动态变换：

```bash
ros2 topic echo /tf --once
```

如果没有，检查 `odom_to_tf` 是否启动：

```bash
ros2 node list | grep odom_to_tf
```

### 4. 相机图像是黑的或看不到障碍物

先确认 Gazebo 还在运行，并让小车对准 `front_box`。也可以在 Gazebo 中手动调整视角，确认障碍物在小车前方。

## 练习

### 练习 1：键盘遥控绕障碍物移动

用终端 2 的键盘控制小车：

- 按 `i` 靠近 `front_box`。
- 按 `j` 或 `l` 原地转向。
- 按 `k` 停止。

观察 Gazebo 与 RViz 是否同步变化。

### 练习 2：同时观察三条链路

启动后打开三个检查命令：

```bash
ros2 topic echo /odom --once
ros2 topic echo /scan --once
ros2 topic echo /camera/camera_info --once
```

分别确认：

- `/odom` 的父子 frame 是 `odom` 和 `base_link`。
- `/scan` 的 frame 是 `laser_link`。
- `/camera/camera_info` 的 frame 是 `camera_optical_frame`。

### 练习 3：画出 TF 树

运行：

```bash
ros2 run tf2_tools view_frames
```

查看生成的 PDF，确认至少包含：

```text
odom
base_link
laser_link
camera_link
camera_optical_frame
```

## 知识问答

问题 1：

```text
为什么键盘 teleop 发布的是 /cmd_vel，而不是直接控制 Gazebo 轮子？
```

参考答案：

```text
ROS 2 控制移动机器人通常使用 geometry_msgs/msg/Twist 表达期望速度。teleop 只负责发布 /cmd_vel，Gazebo 中的 DiffDrive 插件负责把速度命令转换成左右轮运动。
```

问题 2：

```text
/odom 和 /tf 有什么区别？
```

参考答案：

```text
/odom 是里程计消息，里面包含位姿、速度和协方差信息；/tf 是坐标变换流，RViz 和 tf2 用它查询 frame 之间的位置关系。本课用 odom_to_tf 把 /odom 中的位姿转换成 odom -> base_link。
```

问题 3：

```text
为什么传感器消息需要 frame_id？
```

参考答案：

```text
frame_id 告诉 ROS 2 这份数据属于哪个坐标系。LaserScan 如果标记为 laser_link，RViz 才能通过 TF 推导每个激光点在 odom 中的位置。
```

问题 4：

```text
为什么相机使用 camera_optical_frame？
```

参考答案：

```text
ROS 相机图像通常使用 optical frame：x 向右，y 向下，z 指向图像前方。前面 URDF/Xacro 已经建立 camera_link -> camera_optical_frame，本课把相机消息 frame_id 对齐到这个 frame。
```

## 完成标准

完成本课后，你应该能做到：

- 用 `diffbot_sensors_rviz.launch.py` 启动 Gazebo、bridge、TF 和 RViz。
- 用 `ros2 run teleop_twist_keyboard teleop_twist_keyboard` 键盘控制小车运动。
- 在 ROS 2 中看到 `/scan`、`/camera/image_raw`、`/camera/camera_info` 和 `/odom`。
- 在 RViz 中同时看到 RobotModel、TF、LaserScan 和相机图像。
- 能解释 `odom_to_tf` 为什么需要存在。
- 能说明传感器 `frame_id`、TF 和 RViz `Fixed Frame` 的关系。

下一课可以开始为后续感知和导航准备更完整的仿真调试流程。
