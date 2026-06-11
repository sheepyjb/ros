# 第 3 周第 1 小课：tf2 与 ROS 2 坐标系入门

这份文档对应第 3 周第 1 小课：先理解机器人系统中的坐标系，再用 tf2 发布和查询一棵最小 TF 树。

本课目标：

```text
理解 frame、transform、TF 树，以及 map、odom、base_link、camera_link 这些坐标系的基本分工。
```

本课要学：

```text
frame
transform
tf2
/tf
/tf_static
map
odom
base_link
camera_link
tf2_echo
rviz2
TF display
view_frames
TransformBroadcaster
TransformListener
```

本课练习：

```text
创建 tf2_frame_demo 示例包
发布 map -> odom 静态坐标变换
发布 odom -> base_link 动态坐标变换
发布 base_link -> camera_link 静态坐标变换
查询 map -> camera_link 的实时变换
在 RViz2 中观察 TF 坐标轴和父子关系线
生成 TF 树图
```

先记住一句话：

```text
TF 不是控制机器人运动的命令，而是在回答“某个坐标系相对另一个坐标系在哪里”。
```

## 一、为什么机器人系统一定需要坐标系

前两周我们用 turtlesim 做了 P 控制，核心数据只有：

```text
乌龟当前 x/y/theta
目标点 x/y
速度命令 linear/angular
```

真实机器人会复杂很多。它可能同时有：

```text
车体
轮子
摄像头
雷达
机械臂
地图
里程计
目标物体
```

这些东西都要回答类似问题：

```text
摄像头看到的目标点，在车体前方还是左侧？
雷达扫描点，落在地图的什么位置？
机器人底盘，在地图里现在大概在哪里？
```

如果没有统一的坐标关系，每个模块都只能说自己的局部数据，系统无法把它们合起来。

tf2 的作用就是维护这些坐标关系。

## 二、frame 是什么

`frame` 可以理解为一个坐标系的名字。

常见 frame：

```text
map
odom
base_link
camera_link
laser_link
```

每个 frame 都有自己的原点和 x/y/z 轴。

例如 `base_link` 通常表示机器人底盘坐标系：

```text
x 轴：机器人正前方
y 轴：机器人左侧
z 轴：机器人上方
```

`camera_link` 表示摄像头坐标系。它的位置可能在 `base_link` 前方 0.25 米、上方 0.20 米。

所以我们需要表达：

```text
camera_link 相对 base_link 在哪里
```

这就是 transform。

## 三、transform 是什么

`transform` 是两个 frame 之间的位置和姿态关系。

它包含两部分：

```text
translation：平移，单位是米
rotation：旋转，通常用四元数表示
```

在 ROS 2 里，常用消息类型是：

```text
geometry_msgs/msg/TransformStamped
```

里面最关键的是：

```text
header.frame_id
child_frame_id
transform.translation
transform.rotation
```

要特别记住：

```text
header.frame_id 是父坐标系
child_frame_id 是子坐标系
transform 描述“子坐标系在父坐标系中”的位置和姿态
```

例如：

```text
header.frame_id = "base_link"
child_frame_id = "camera_link"
translation.x = 0.25
translation.z = 0.20
```

含义是：

```text
camera_link 的原点，在 base_link 坐标系下，向前 0.25 米，向上 0.20 米。
```

## 四、TF 树是什么

多个 transform 连起来，就形成 TF 树。

本课示例使用这棵树：

```text
map
└── odom
    └── base_link
        └── camera_link
```

对应关系：

```text
map -> odom
odom -> base_link
base_link -> camera_link
```

tf2 可以沿着这棵树自动推导间接关系。

例如我们只发布了：

```text
map -> odom
odom -> base_link
base_link -> camera_link
```

但仍然可以查询：

```text
map -> camera_link
```

因为 tf2 会沿着树把中间关系串起来。

## 五、map、odom、base_link 的基本分工

### map

`map` 通常表示全局地图坐标系。

特点：

```text
长期稳定
适合表达全局位置
可能会因为定位修正而产生跳变
```

例如导航时说：

```text
机器人在地图中的位置
目标点在地图中的位置
```

一般会用 `map`。

### odom

`odom` 通常表示里程计坐标系。

特点：

```text
短时间连续
不会突然跳变
长期会漂移
```

轮速计、视觉里程计、惯性测量等都可能贡献 `odom -> base_link`。

### base_link

`base_link` 通常表示机器人底盘坐标系。

特点：

```text
跟着机器人一起移动
控制算法常用它表达“前方、左侧、右侧”
```

例如 `/cmd_vel` 的线速度 `linear.x`，通常可以理解成沿机器人自身 `base_link` 的 x 轴前进。

### camera_link

`camera_link` 通常表示摄像头坐标系。

特点：

```text
固定安装在机器人上
位置相对 base_link 通常不变
后续接 YOLO 时很重要
```

以后如果 YOLO 在图像里发现目标，我们要进一步思考：

```text
这个目标在 camera_link 下在哪里？
它换算到 base_link 或 map 下在哪里？
```

这就是 tf2 后面会发挥作用的地方。

## 六、静态 transform 和动态 transform

TF 分两类：

```text
静态 transform
动态 transform
```

静态 transform 表示长期不变的关系。

例子：

```text
base_link -> camera_link
```

摄像头用螺丝固定在车体上，只要不重新安装，它相对车体的位置不变。

动态 transform 表示会随时间变化的关系。

例子：

```text
odom -> base_link
```

机器人在运动，所以底盘相对里程计坐标系的位置一直在变。

ROS 2 中常见话题：

```text
/tf_static：静态 transform
/tf：动态 transform
```

## 七、本课示例包结构

本课新增 package：

```text
src/tf2_frame_demo/
├── README.md
├── WEEK_03_01_TF2_FRAMES.md
├── launch/
│   └── tf2_demo.launch.py
├── package.xml
├── resource/
│   └── tf2_frame_demo
├── setup.cfg
├── setup.py
├── test/
│   ├── test_frame_math.py
│   └── test_tf2_frame_demo_assets.py
└── tf2_frame_demo/
    ├── __init__.py
    ├── dynamic_frame_broadcaster.py
    ├── frame_listener.py
    └── frame_math.py
```

分工：

```text
frame_math.py
= 纯数学函数
= 计算圆周运动位姿和 yaw 四元数

dynamic_frame_broadcaster.py
= 发布 odom -> base_link 动态 TF

frame_listener.py
= 查询 map -> camera_link，并打印位置和 yaw

tf2_demo.launch.py
= 一次启动静态 TF、动态 TF 和 listener
```

## 八、frame_math.py 解释

`frame_math.py` 不依赖 ROS 2，方便测试。

它做两件事：

```text
1. 根据 yaw 角生成四元数
2. 生成一个绕圆运动的平面位姿
```

为什么要单独拆出来？

```text
数学逻辑可以不用启动 ROS 2 节点就验证。
```

这和第 1 周把 P 控制数学拆到 `controller_math.py` 是同一个思路。

## 九、dynamic_frame_broadcaster.py 解释

这个节点发布：

```text
odom -> base_link
```

它让 `base_link` 绕一个圆运动。

所以你后面用 `tf2_echo map camera_link` 会看到 `x/y/yaw` 一直变化。

关键对象：

```text
TransformBroadcaster
TransformStamped
```

关键字段：

```text
transform.header.frame_id = "odom"
transform.child_frame_id = "base_link"
```

意思是：

```text
base_link 在 odom 坐标系下的位置和姿态。
```

## 十、frame_listener.py 解释

这个节点查询：

```text
map -> camera_link
```

也就是：

```text
camera_link 在 map 坐标系下的位置和姿态。
```

关键对象：

```text
Buffer
TransformListener
lookup_transform
```

listener 本身不计算 TF 树，它只是向 tf2 buffer 查询：

```text
target_frame = "map"
source_frame = "camera_link"
```

如果中间关系完整：

```text
map -> odom -> base_link -> camera_link
```

tf2 就能返回结果。

如果中间缺一段，比如没有 `base_link -> camera_link`，查询会失败。

## 十一、构建和运行

终端 1：

```bash
cd ~/ros
source /opt/ros/jazzy/setup.bash
colcon build --packages-select tf2_frame_demo
source install/setup.bash
ros2 launch tf2_frame_demo tf2_demo.launch.py
```

你应该能看到 listener 持续打印类似：

```text
map -> camera_link: x=..., y=..., yaw=...
```

终端 2：

```bash
cd ~/ros
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run tf2_ros tf2_echo map camera_link
```

它会持续输出 `map` 和 `camera_link` 的变换关系。

终端 3：

```bash
cd ~/ros
source /opt/ros/jazzy/setup.bash
source install/setup.bash
rviz2
```

RViz2 打开后：

```text
1. 左侧 Displays 面板中，找到 Global Options
2. 把 Fixed Frame 改成 map
3. 点击左下角 Add
4. 选择 By display type
5. 添加 TF
6. 展开 TF，确认 Show Names、Show Axes、Show Arrows 都勾选
```

你应该能看到：

```text
map 和 odom 基本重合
base_link 绕 odom 运动
camera_link 靠近 base_link，并跟着 base_link 一起运动
黄色线表示 TF 父子关系
```

如果关闭 RViz2 时提示是否保存：

```text
There are unsaved changes.
```

本课选择：

```text
Discard
```

原因是这次只是临时观察 TF。正式 RViz 配置会在后续 `robot_description` 小课保存到项目文件里。

终端 4：

```bash
cd ~/ros
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run tf2_tools view_frames
```

它会生成 TF 树 PDF，一般文件名是：

```text
frames.pdf
```

## 十二、RViz2 里看到的是什么

RViz2 里这节课看到的是：

```text
坐标轴
frame 名字
TF 父子关系线
```

还不是：

```text
机器人外壳
轮子模型
摄像头外形
雷达外形
真实相机画面
```

原因是：

```text
我们还没有写 URDF
```

本课的 `base_link` 只是“底盘坐标系”，不是底盘模型。

本课的 `camera_link` 只是“摄像头安装位置的坐标系”，不是摄像头画面。

如果你看到 `map` 和 `odom` 重合，这是正常的。因为本课发布的：

```text
map -> odom
```

是 0 平移、0 旋转，所以两个坐标系完全叠在一起。

如果你看到 `base_link` 和 `camera_link` 很近，也是正常的。因为本课设置的是：

```text
base_link -> camera_link
x = 0.25
z = 0.20
```

意思是摄像头安装在底盘前方 0.25 米、上方 0.20 米。

## 十三、单独体验 static_transform_publisher

如果你只想手动发布一个静态 TF，可以运行：

```bash
ros2 run tf2_ros static_transform_publisher \
  --x 0.25 --y 0.0 --z 0.20 \
  --roll 0.0 --pitch 0.0 --yaw 0.0 \
  --frame-id base_link \
  --child-frame-id camera_link
```

这条命令表达：

```text
camera_link 在 base_link 前方 0.25 米、上方 0.20 米。
```

参数里最重要的是：

```text
--frame-id：父坐标系
--child-frame-id：子坐标系
```

## 十四、常见错误

### 错误 1：把父子 frame 写反

如果你想表达：

```text
camera_link 安装在 base_link 上
```

通常应该写：

```text
base_link -> camera_link
```

不要写成：

```text
camera_link -> base_link
```

写反以后，tf2 仍然可能有数据，但物理含义会错。

### 错误 2：TF 树断开

如果只发布：

```text
odom -> base_link
base_link -> camera_link
```

但没有：

```text
map -> odom
```

那么查询：

```text
map -> camera_link
```

就会失败。

### 错误 3：同一个 child_frame 有多个父节点

TF 树要求一个 child frame 只能有一个直接父节点。

不要同时发布：

```text
odom -> base_link
map -> base_link
```

这会让 TF 树含义混乱。

## 十五、练习题

### 练习 1：查看本课 package

构建后运行：

```bash
ros2 pkg executables tf2_frame_demo
```

你应该看到：

```text
tf2_frame_demo dynamic_frame_broadcaster
tf2_frame_demo frame_listener
```

### 练习 2：启动 TF 示例

运行：

```bash
ros2 launch tf2_frame_demo tf2_demo.launch.py
```

观察 listener 输出的 `x/y/yaw` 是否在变化。

### 练习 3：查看动态 TF 话题

运行：

```bash
ros2 topic echo /tf --once
```

观察里面是否有：

```text
frame_id: odom
child_frame_id: base_link
```

### 练习 4：查看静态 TF 话题

运行：

```bash
ros2 topic echo /tf_static --once
```

观察里面是否有：

```text
frame_id: map
child_frame_id: odom
```

以及：

```text
frame_id: base_link
child_frame_id: camera_link
```

### 练习 5：用 tf2_echo 查询间接关系

运行：

```bash
ros2 run tf2_ros tf2_echo map camera_link
```

思考：

```text
我们没有直接发布 map -> camera_link，为什么能查到？
```

### 练习 6：用 RViz2 可视化 TF

运行：

```bash
rviz2
```

在 RViz2 中完成：

```text
Fixed Frame = map
Add -> TF
Show Names = true
Show Axes = true
Show Arrows = true
```

观察：

```text
map 和 odom 是否重合
base_link 是否绕 odom 运动
camera_link 是否跟着 base_link 运动
```

关闭 RViz2 时，如果提示保存，选择：

```text
Discard
```

### 练习 7：生成 TF 树图

运行：

```bash
ros2 run tf2_tools view_frames
```

打开或查看生成的 `frames.pdf`，确认是否能看到：

```text
map -> odom -> base_link -> camera_link
```

### 练习 8：修改摄像头安装位置

打开：

```text
src/tf2_frame_demo/launch/tf2_demo.launch.py
```

把 `base_link -> camera_link` 的 `--x` 从 `0.25` 改成 `0.50`。

重新构建并运行后，观察：

```bash
ros2 run tf2_ros tf2_echo map camera_link
```

看 `camera_link` 的位置是否发生变化。

### 练习 9：运行测试

运行：

```bash
source /opt/ros/jazzy/setup.bash
PYTHONPATH=src/tf2_frame_demo:$PYTHONPATH python3 -m unittest discover -s src/tf2_frame_demo/test
```

这一步不需要启动 ROS 2 节点，主要检查数学函数和 package 资产。

## 十六、参考答案要点

### 练习 1

如果 `ros2 pkg executables tf2_frame_demo` 找不到包，通常是：

```text
没有 colcon build
没有 source install/setup.bash
```

### 练习 2

`x/y/yaw` 会变化，因为 `dynamic_frame_broadcaster` 在持续发布：

```text
odom -> base_link
```

而 `camera_link` 固定在 `base_link` 上，所以 `camera_link` 也会跟着移动。

### 练习 3

`/tf` 是动态 TF 话题，适合 `odom -> base_link` 这种随时间变化的关系。

### 练习 4

`/tf_static` 是静态 TF 话题，适合：

```text
map -> odom
base_link -> camera_link
```

这种长期不变的关系。

### 练习 5

因为 tf2 可以沿 TF 树推导间接关系：

```text
map -> odom -> base_link -> camera_link
```

所以即使没有直接发布 `map -> camera_link`，也能查询出来。

### 练习 6

RViz2 中看到的是坐标系，不是机器人外观。

其中：

```text
map 和 odom 重合，因为 map -> odom 是 0 平移、0 旋转
base_link 绕 odom 运动，因为 odom -> base_link 是动态 TF
camera_link 跟着 base_link 运动，因为 base_link -> camera_link 是静态 TF
黄色线表示 TF 父子关系
```

关闭时选择 `Discard`，因为本课不保存临时 RViz 配置。

### 练习 7

TF 树应该是一棵连通树，而不是几段互不相连的关系。

### 练习 8

`--x` 变大后，表示摄像头安装得更靠前。查询 `map -> camera_link` 时，位置会相对 `base_link` 多出这段偏移。

### 练习 9

测试会检查：

```text
yaw 到四元数的转换
圆周运动位姿计算
launch 文件是否存在
setup.py 是否安装 launch 文件
package.xml 是否声明 tf2 依赖
Ctrl-C 退出路径是否干净
```

## 十七、知识问答

### 问 1：TF 和 topic 有什么关系？

TF 数据本质上也通过 topic 传播，主要是：

```text
/tf
/tf_static
```

但你平时更常用 tf2 API 查询坐标关系，而不是直接手写订阅 `/tf`。

### 问 2：为什么 rotation 常用四元数，而不是 yaw？

因为三维空间的姿态包含 roll、pitch、yaw。四元数更适合表达三维旋转，也能避免一些欧拉角奇异问题。

本课主要在平面内运动，所以只从 yaw 生成四元数。

### 问 3：map 和 odom 到底谁更准？

不能简单说谁更准。

`odom` 短时间连续，适合控制；但长期会漂移。

`map` 更接近全局定位结果，适合导航；但定位修正时可能跳变。

### 问 4：base_link 和 base_footprint 有什么区别？

常见约定是：

```text
base_link：机器人底盘三维坐标系
base_footprint：机器人投影到地面的二维坐标系
```

本课先只用 `base_link`，后面进入 URDF / Nav2 时再补 `base_footprint`。

### 问 5：为什么 TF 树不能让一个 child 有两个父节点？

因为同一个坐标系如果同时由两个父坐标系直接定义，系统就不知道哪条关系才是权威来源。

例如不要同时发布：

```text
odom -> base_link
map -> base_link
```

一般做法是发布：

```text
map -> odom
odom -> base_link
```

## 十八、通过标准

完成本课后，你应该能做到：

```text
能解释 frame 和 transform 的区别
能说清 header.frame_id 和 child_frame_id 的含义
能画出 map -> odom -> base_link -> camera_link
能区分 /tf 和 /tf_static
能用 tf2_echo 查询两个 frame 之间的关系
能在 RViz2 中添加 TF display 并观察坐标轴运动
能解释 RViz2 里看到的是坐标系，不是机器人模型
能解释为什么没有直接发布 map -> camera_link 也能查到它
能理解 camera_link 为什么通常固定挂在 base_link 下面
```

如果这些都能说清楚，就可以进入第 3 周第 2 小课：`robot_description`、URDF / Xacro 和 RViz。
