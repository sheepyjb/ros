# 第 3 周第 2 小课：robot_description、URDF、轮子、摄像头和雷达 frame

这份文档对应第 3 周第 2 小课：创建 `robot_description` 包，用 URDF 描述一台简化差速小车，并在 RViz2 中观察机器人模型和 TF。

本课目标：

```text
理解 robot_description 包、URDF、link、joint，以及轮子、摄像头、雷达 frame 如何通过 robot_state_publisher 变成 TF。
```

本课要学：

```text
robot_description
URDF
link
joint
robot_state_publisher
RobotModel display
base_link
left_wheel_link
right_wheel_link
camera_link
camera_optical_frame
laser_link
```

本课练习：

```text
创建 robot_description 包
编写 diffbot.urdf
用 robot_state_publisher 发布 URDF 中的 TF
用 RViz2 同时观察 RobotModel 和 TF
用 tf2_echo 检查传感器 frame
```

先记住一句话：

```text
URDF 描述“机器人由哪些 link 组成，以及这些 link 之间通过什么 joint 连接”。
```

## 一、robot_description 包是什么

`robot_description` 通常是一个资源包，不负责控制算法，也不负责传感器数据处理。

它主要保存：

```text
机器人模型文件：URDF / Xacro
可视化配置：RViz 配置
模型显示启动文件：launch
```

本课创建的包结构是：

```text
src/robot_description/
├── launch/
│   └── display.launch.py
├── rviz/
│   └── display.rviz
├── urdf/
│   └── diffbot.urdf
├── package.xml
└── setup.py
```

这个包的边界很清楚：

```text
robot_description：描述机器人长什么样、frame 怎么连
robot_bringup：后续负责统一启动多个包
tf2_frame_demo：上一课用于手写 TF 的入门示例
```

## 二、URDF 的核心：link 和 joint

URDF 里最重要的是两个概念。

`link` 表示机器人上的一个刚体或坐标系，例如：

```text
base_link
left_wheel_link
right_wheel_link
camera_link
laser_link
```

`joint` 表示两个 link 之间的连接关系，例如：

```text
base_link -> left_wheel_link
base_link -> camera_link
base_link -> laser_link
```

每个 joint 都有：

```text
parent link：父 link
child link：子 link
origin：子 link 在父 link 下的位置和姿态
type：固定、连续旋转、有限角度旋转等
```

本课最关键的区别：

```text
fixed joint：固定安装，不需要 /joint_states，例如 wheel_joint、camera_joint、laser_joint
continuous joint：可连续旋转，需要 /joint_states，本课暂不使用，后续 Gazebo 和控制课再引入
```

## 三、本课机器人模型

本课模型叫 `diffbot`，表示一个简化差速小车。

TF/link 关系：

```text
base_link
├── left_wheel_link          left_wheel_joint，fixed
├── right_wheel_link         right_wheel_joint，fixed
├── camera_link              camera_joint，fixed
│   └── camera_optical_frame camera_optical_joint，fixed
└── laser_link               laser_joint，fixed
```

`base_link` 是底盘坐标系：

```text
x 轴：机器人前方
y 轴：机器人左侧
z 轴：机器人上方
```

`camera_link` 是摄像头物理安装 frame。

`camera_optical_frame` 是相机光学 frame，常用于图像算法：

```text
z 轴：相机看出去的方向
x 轴：图像右方
y 轴：图像下方
```

`laser_link` 是雷达 frame，后续 `/scan` 消息的 `header.frame_id` 通常会写成这个名字。

## 四、robot_state_publisher 做什么

`robot_state_publisher` 读取 URDF，然后发布 TF。

它的工作可以理解成：

```text
URDF 提供 link/joint 拓扑和固定安装尺寸
robot_state_publisher 把 fixed joint 转换成 /tf_static
```

本课里：

```text
left_wheel_joint、right_wheel_joint、camera_joint、laser_joint 都是 fixed，会进入 /tf_static
```

这一课先把轮子也当成固定安装的 frame，重点理解 URDF 如何生成 TF。轮子真实旋转和 `/joint_states` 会在后续 Gazebo 和控制课程里再引入。

## 五、运行本课

在仓库根目录运行：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select robot_description
source install/setup.bash
ros2 launch robot_description display.launch.py
```

正常会启动两个进程：

```text
robot_state_publisher
rviz2
```

RViz2 已经加载 `display.rviz`，重点看两个 display：

```text
RobotModel：显示 URDF 里的机器人外形
TF：显示每个 frame 的坐标轴和名字
```

观察问题：

```text
1. RobotModel 里能不能看到底盘、两个轮子、摄像头和雷达？
2. TF 里能不能看到 base_link、camera_link、camera_optical_frame、laser_link？
3. 左右轮 frame 是否都挂在 base_link 下面？
```

## 六、用命令行检查 TF

新开一个终端：

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

查看摄像头相对底盘的位置：

```bash
ros2 run tf2_ros tf2_echo base_link camera_link
```

查看雷达相对底盘的位置：

```bash
ros2 run tf2_ros tf2_echo base_link laser_link
```

查看相机光学 frame：

```bash
ros2 run tf2_ros tf2_echo camera_link camera_optical_frame
```

生成 TF 树图：

```bash
ros2 run tf2_tools view_frames
```

如果生成了类似 `frames_*.pdf` 的文件，就说明 TF 树可以被工具读取。

## 七、为什么这一课不写手动 TF broadcaster

上一课我们手写了：

```text
static_transform_publisher
TransformBroadcaster
TransformListener
```

那是为了理解 TF 的底层概念。

真实机器人模型里，轮子、摄像头、雷达这些结构关系不应该分散写在多个 TF broadcaster 里，而应该集中写进 URDF。这样做有三个好处：

```text
模型结构集中管理
RViz 可以直接显示 RobotModel
后续 Gazebo、Nav2、MoveIt2 都能复用同一份机器人描述
```

## 八、本课练习题

练习 1：

```text
把 camera_joint 的 x 从 0.22 改成 0.30，重新 build/source/launch，观察 camera_link 是否更靠前。
```

练习 2：

```text
把 laser_joint 的 z 从 0.25 改成 0.30，观察 laser_link 是否更高。
```

练习 3：

```text
用 tf2_echo 分别查看 base_link -> camera_link 和 base_link -> laser_link，解释 translation 的 x/y/z 各代表什么。
```

## 九、知识问答

问题 1：

```text
URDF 里的 link 和 TF 里的 frame 是什么关系？
```

参考答案：

```text
URDF 的 link 会被 robot_state_publisher 转换成 TF frame。link 之间的 joint 关系决定 TF 树里的父子关系。
```

问题 2：

```text
为什么本课把 wheel_joint、camera_joint、laser_joint 都写成 fixed？
```

参考答案：

```text
这一课重点是观察 frame 的安装关系，不模拟轮子转动；fixed joint 不依赖 /joint_states，更适合先理解 URDF 到 TF 的转换。
```

问题 3：

```text
robot_state_publisher 负责什么？
```

参考答案：

```text
robot_state_publisher 根据 URDF 中的 link/joint 关系发布 TF。本课所有 joint 都是 fixed，因此它主要发布 /tf_static。
```

问题 4：

```text
为什么还要有 camera_optical_frame？
```

参考答案：

```text
机器人底盘和普通 link 常用 x 前、y 左、z 上；相机图像算法常用 z 前、x 右、y 下。camera_optical_frame 用来表达这个光学坐标约定。
```

## 十、完成标准

完成本课后，你应该能做到：

```text
能说明 robot_description 包的职责
能解释 URDF 中 link 和 joint 的含义
能解释为什么本课先用 fixed joint 表达轮子、摄像头和雷达 frame
能在 RViz2 中同时看到 RobotModel 和 TF
能用 tf2_echo 查看 base_link 到 camera_link / laser_link 的变换
能说清楚 robot_state_publisher 为什么能根据 URDF 发布 TF
```

下一课会继续把 URDF 改成 Xacro，并把模型显示接入更完整的启动流程。
