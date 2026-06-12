# 第 3 周第 3 小课：Xacro、可复用 RViz/bringup 启动和模型组织

这份文档对应第 3 周第 3 小课：把上一课的 `diffbot.urdf` 改造成可复用的 Xacro 模型，并让 `robot_bringup` 成为更统一的模型显示入口。

本课目标：

```text
理解 Xacro 如何减少 URDF 重复内容，并掌握 robot_description 与 robot_bringup 的职责分工。
```

本课要学：

```text
Xacro
xacro:property
xacro:macro
xacro:include
robot_description
robot_bringup
IncludeLaunchDescription
robot_state_publisher
RViz2
```

本课练习：

```text
把 diffbot.urdf 改造成 diffbot.urdf.xacro
把材质和组件宏拆成可复用 Xacro 文件
让 display.launch.py 从 Xacro 生成 robot_description
新增 robot_bringup/launch/display_robot.launch.py 作为统一显示入口
```

先记住一句话：

```text
Xacro 不是新的机器人描述格式，而是“生成 URDF 的模板语言”。
```

## 一、为什么要用 Xacro

上一课的 `diffbot.urdf` 能正常显示模型，但它有一个明显问题：很多结构重复。

例如左右轮几乎一样：

```text
link 结构一样
visual/collision 几何一样
inertial 近似一样
joint 结构一样
只有名字和 y 方向安装位置不同
```

如果继续只写普通 URDF，后续增加四个轮子、多个传感器、Gazebo 插件时，文件会越来越长，也更容易改漏。

Xacro 解决的是这个问题：

```text
用 property 保存尺寸和安装位置
用 macro 复用重复结构
用 include 拆分模型文件
最后仍然生成普通 URDF
```

## 二、本课新的模型文件组织

本课保留上一课的 `diffbot.urdf`，作为普通 URDF 对照文件。

新增 Xacro 文件：

```text
src/robot_description/urdf/
├── diffbot.urdf
├── diffbot.urdf.xacro
├── diffbot_materials.xacro
└── diffbot_components.xacro
```

它们的职责是：

```text
diffbot.urdf：上一课普通 URDF，对照学习用
diffbot.urdf.xacro：本课顶层模型入口
diffbot_materials.xacro：集中定义颜色材质
diffbot_components.xacro：集中定义轮子、摄像头、雷达组件宏
```

这样做的好处是：

```text
尺寸参数集中在顶层文件
颜色材质不会散落在每个 link 里
重复的轮子结构只写一次
后续添加传感器时有明确位置可放
```

## 三、property：把尺寸变成参数

`diffbot.urdf.xacro` 里有类似这样的参数：

```xml
<xacro:property name="body_length" value="0.42"/>
<xacro:property name="wheel_radius" value="0.07"/>
<xacro:property name="camera_x" value="0.22"/>
<xacro:property name="laser_z" value="0.25"/>
```

它们的作用是把数字集中命名。

例如车体尺寸不再散落成：

```xml
<box size="0.42 0.30 0.16"/>
```

而是写成：

```xml
<box size="${body_length} ${body_width} ${body_height}"/>
```

这样你以后看到 `camera_x`，就知道它是摄像头相对 `base_link` 的前后安装位置，而不是一个没有语义的 `0.22`。

## 四、macro：把重复结构变成模板

`diffbot_components.xacro` 里定义了轮子宏：

```xml
<xacro:macro name="diffbot_wheel" params="side y_offset radius width mass">
  ...
</xacro:macro>
```

顶层模型里调用两次：

```xml
<xacro:diffbot_wheel side="left" y_offset="${wheel_y_offset}" .../>
<xacro:diffbot_wheel side="right" y_offset="${-wheel_y_offset}" .../>
```

这两次调用会生成：

```text
left_wheel_link
left_wheel_joint
right_wheel_link
right_wheel_joint
```

也就是说，宏不是运行时节点，也不是 TF 发布器；它只是在启动前把模板展开成普通 URDF 内容。

## 五、include：把模型拆成多个文件

顶层文件中有：

```xml
<xacro:include filename="diffbot_materials.xacro"/>
<xacro:include filename="diffbot_components.xacro"/>
```

`include` 的含义是：

```text
把别的 Xacro 文件内容引入当前模型
```

本课用它把模型拆成三类内容：

```text
顶层文件：决定机器人有哪些组件，以及主要尺寸是多少
材质文件：决定颜色
组件文件：决定重复结构如何生成
```

## 六、display.launch.py 现在做什么

上一课 `display.launch.py` 直接读取 `diffbot.urdf`：

```text
diffbot.urdf -> robot_state_publisher
```

本课改成：

```text
diffbot.urdf.xacro -> xacro 展开 -> robot_description 参数 -> robot_state_publisher
```

核心关系没有变：

```text
robot_state_publisher 仍然只接收 robot_description
RViz2 仍然通过 /robot_description 和 TF 显示模型
```

变的是模型来源：从手写完整 URDF，变成由 Xacro 生成 URDF。

## 七、robot_bringup 的新入口

本课新增：

```text
src/robot_bringup/launch/display_robot.launch.py
```

它不重新写 `robot_state_publisher` 和 RViz2 的细节，而是 include `robot_description` 包里的显示 launch：

```text
robot_bringup/display_robot.launch.py
└── robot_description/display.launch.py
    ├── robot_state_publisher
    └── rviz2
```

这体现了两个包的职责边界：

```text
robot_description：知道机器人模型文件、RViz 配置在哪里
robot_bringup：知道要把哪些功能包组合起来启动
```

后续系统变复杂后，你会更常从 `robot_bringup` 启动，而不是分别记住每个功能包的 launch 文件。

## 八、运行本课

确认已安装 Xacro：

```bash
source /opt/ros/jazzy/setup.bash
ros2 pkg prefix xacro
```

注意：当前 Jazzy 的 `xacro` 命令不支持 `xacro --version`，能用 `ros2 pkg prefix xacro` 查到包路径即可。

在仓库根目录构建：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select robot_description robot_bringup
source install/setup.bash
```

推荐从 bringup 入口启动：

```bash
ros2 launch robot_bringup display_robot.launch.py
```

也可以直接启动模型包入口：

```bash
ros2 launch robot_description display.launch.py
```

命令行单独检查 Xacro 展开结果：

```bash
xacro src/robot_description/urdf/diffbot.urdf.xacro
```

如果输出里能看到普通的 `<link>` 和 `<joint>`，说明 Xacro 已经被展开成 URDF。

## 九、观察问题

启动 RViz2 后观察：

```text
1. RobotModel 是否仍然能看到底盘、左右轮、摄像头和雷达？
2. TF 中是否仍然有 base_link、left_wheel_link、right_wheel_link、camera_link、camera_optical_frame、laser_link？
3. 用 bringup 启动和直接启动 robot_description，RViz 里看到的模型是否一致？
```

再用命令行检查：

```bash
ros2 run tf2_ros tf2_echo base_link camera_link
ros2 run tf2_ros tf2_echo base_link laser_link
```

你应该看到和上一课相同的安装位置。

## 十、本课练习题

练习 1：

```text
把 diffbot.urdf.xacro 里的 camera_x 从 0.22 改成 0.30，重新 build/source/launch，观察摄像头是否更靠前。
```

练习 2：

```text
把 wheel_radius 从 0.07 改成 0.09，观察两个轮子的半径和 wheel joint 的 z 位置是否一起变化。
```

练习 3：

```text
把 laser_z 从 0.25 改成 0.30，观察 laser_link 是否更高。
```

练习 4：

```text
分别运行 robot_description/display.launch.py 和 robot_bringup/display_robot.launch.py，解释为什么两个入口显示的是同一个模型。
```

## 十一、知识问答

问题 1：

```text
Xacro 和 URDF 是什么关系？
```

参考答案：

```text
Xacro 是生成 URDF 的模板语言。robot_state_publisher 最终接收的仍然是展开后的 URDF 字符串，而不是未展开的模板概念。
```

问题 2：

```text
为什么要用 xacro:property？
```

参考答案：

```text
property 可以给尺寸、质量、安装位置等数字命名。这样修改模型时更集中，也更容易理解每个数字代表什么。
```

问题 3：

```text
为什么左右轮适合用 xacro:macro？
```

参考答案：

```text
左右轮结构几乎一样，只是名字和 y 方向安装位置不同。用 macro 可以避免复制两大段 URDF，降低改漏和改错的概率。
```

问题 4：

```text
robot_description 和 robot_bringup 的职责有什么区别？
```

参考答案：

```text
robot_description 负责保存和发布机器人模型相关资产，例如 URDF/Xacro、RViz 配置和模型显示 launch。robot_bringup 负责把多个功能包组合起来启动，是系统级入口。
```

问题 5：

```text
为什么 robot_bringup/display_robot.launch.py 要 include robot_description/display.launch.py，而不是复制一遍节点配置？
```

参考答案：

```text
include 可以复用已有 launch，避免同一套 robot_state_publisher 和 RViz2 配置在多个地方重复。以后模型显示方式改变时，只需要改 robot_description 的显示入口。
```

## 十二、完成标准

完成本课后，你应该能做到：

```text
能解释 Xacro 最终会展开成 URDF
能说明 property、macro、include 各自解决什么问题
能说出本课三个 Xacro 文件的职责
能用 xacro 命令检查 diffbot.urdf.xacro 展开结果
能从 robot_bringup 启动 RViz2 模型显示
能解释 robot_description 和 robot_bringup 的边界
```

下一课可以继续把模型接入 Gazebo 前置准备，或先补充 joint_state_publisher 与可动轮子 joint。
