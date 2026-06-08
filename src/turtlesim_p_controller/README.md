# turtlesim_p_controller

第 1 周练习：用 P 控制让 turtlesim 乌龟移动到固定目标点。

如果你是 0 基础，先读 [CODE_WALKTHROUGH.md](CODE_WALKTHROUGH.md)，里面按目录、文件和代码逐行解释这个包。

## 这个文件夹是什么

`/home/sheepyjb/ros/src/turtlesim_p_controller` 是一个 ROS 2 Python package。它不是整个 ROS 2 项目，而是 workspace 里的一个功能包。

整体关系：

```text
/home/sheepyjb/ros                  # ROS 2 workspace
└── src/
    └── turtlesim_p_controller/     # 当前 package
```

ROS 2 的基本组织方式是：

```text
workspace -> src -> package -> node
```

当前包里只有一个主要节点：

```text
turtle_goal_controller
```

它的作用是订阅 turtlesim 的位姿，计算速度命令，然后让乌龟移动到目标点。

## 目录结构

```text
turtlesim_p_controller/
├── package.xml
├── setup.py
├── setup.cfg
├── README.md
├── resource/
│   └── turtlesim_p_controller
├── turtlesim_p_controller/
│   ├── __init__.py
│   ├── controller_math.py
│   └── turtle_goal_controller.py
└── test/
    └── test_controller_math.py
```

运行 Python 后可能还会看到 `__pycache__/`。这是 Python 自动生成的缓存目录，不是 ROS 2 项目源码，不需要手动编辑，也不会提交到 git。

## 每个文件和文件夹的作用

### `package.xml`

这是 ROS 2 package 的元信息文件。ROS 2 和 `colcon` 会通过它知道：

- 包名是什么：`turtlesim_p_controller`
- 包版本是多少：`0.1.0`
- 这个包依赖哪些 ROS 2 包
- 这个包使用哪种构建类型

当前依赖：

```xml
<depend>geometry_msgs</depend>
<depend>rclpy</depend>
<depend>turtlesim</depend>
```

含义：

- `rclpy`：ROS 2 的 Python 客户端库，用来写 Python 节点。
- `geometry_msgs`：提供 `Twist` 速度消息，用来发布 `/turtle1/cmd_vel`。
- `turtlesim`：提供 `Pose` 位姿消息，也提供 `turtlesim_node`。

这一段很重要：

```xml
<export>
  <build_type>ament_python</build_type>
</export>
```

它告诉 ROS 2：这是一个 Python 包，用 `ament_python` 方式构建。

### `setup.py`

这是 Python 包的安装配置文件。`colcon build` 构建这个包时，会读取它。

最关键的是这里：

```python
entry_points={
    "console_scripts": [
        "turtle_goal_controller = turtlesim_p_controller.turtle_goal_controller:main",
    ],
}
```

它定义了一个可执行命令：

```text
turtle_goal_controller
```

所以构建并 `source install/setup.bash` 之后，就可以运行：

```bash
ros2 run turtlesim_p_controller turtle_goal_controller
```

这条命令的含义是：

```text
ros2 run <包名> <可执行入口>
```

也就是：

```text
ros2 run turtlesim_p_controller turtle_goal_controller
```

最终会调用：

```python
turtlesim_p_controller.turtle_goal_controller:main
```

### `setup.cfg`

这个文件告诉 Python 安装工具：脚本应该安装到哪里。

当前内容：

```ini
[develop]
script_dir=$base/lib/turtlesim_p_controller
[install]
install_scripts=$base/lib/turtlesim_p_controller
```

这能让 ROS 2 按 package 的方式找到可执行脚本。

### `resource/turtlesim_p_controller`

这是一个包索引标记文件。内容可以为空，但文件本身需要存在。

`setup.py` 中这一行会安装它：

```python
("share/ament_index/resource_index/packages", ["resource/" + package_name])
```

ROS 2 通过 ament index 发现已经安装的 package。简单说，这个文件帮助 ROS 2 知道：

```text
系统里有一个叫 turtlesim_p_controller 的包
```

### `turtlesim_p_controller/`

这是 Python 源码目录。注意它和外层文件夹同名：

```text
src/turtlesim_p_controller/                 # ROS 2 package 目录
src/turtlesim_p_controller/turtlesim_p_controller/  # Python 模块目录
```

外层是 ROS 2 package，内层是 Python import 用的模块。

### `turtlesim_p_controller/__init__.py`

这个文件让 Python 把当前目录识别为一个 package。

有了它，代码才能这样导入：

```python
from turtlesim_p_controller.controller_math import compute_velocity_command
```

### `turtlesim_p_controller/controller_math.py`

这是控制算法文件，不直接依赖 ROS 2。

它负责：

- 保存控制参数：`ControllerConfig`
- 保存乌龟位姿：`TurtlePose`
- 保存速度命令：`VelocityCommand`
- 归一化角度：`normalize_angle`
- 根据当前位姿和目标点计算速度：`compute_velocity_command`

核心控制逻辑：

```text
当前位置 + 目标点 -> 距离误差和角度误差 -> linear.x 和 angular.z
```

这里故意不写 ROS 2 代码，原因是控制算法可以独立测试。这样即使不开 turtlesim，也能验证数学逻辑是否正确。

### `turtlesim_p_controller/turtle_goal_controller.py`

这是 ROS 2 节点文件。

它负责和 ROS 2 系统通信：

- 创建节点：`turtle_goal_controller`
- 声明参数：`goal_x`、`goal_y`、`linear_gain` 等
- 订阅 `/turtle1/pose`
- 发布 `/turtle1/cmd_vel`
- 调用 `controller_math.py` 计算速度

运行时的数据流：

```text
turtlesim_node
  发布 /turtle1/pose
        ↓
turtle_goal_controller.py
  读取当前位置
  调用 controller_math.py 计算速度
        ↓
  发布 /turtle1/cmd_vel
        ↓
turtlesim_node
  更新乌龟运动
```

### `test/test_controller_math.py`

这是单元测试文件。

它测试的是 `controller_math.py`，不测试 ROS 2 图形窗口。

当前测试覆盖：

- 角度归一化是否正确。
- 目标在正前方时，线速度是否大于 0。
- 目标在左上方时，角速度方向是否正确。
- 已经接近目标点时，是否停止运动。

运行测试：

```bash
cd /home/sheepyjb/ros
PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test
```

## 构建之后发生了什么

执行：

```bash
cd /home/sheepyjb/ros
source /opt/ros/jazzy/setup.bash
colcon build --packages-select turtlesim_p_controller
```

`colcon` 会读取：

```text
package.xml
setup.py
setup.cfg
```

然后生成：

```text
/home/sheepyjb/ros/build/
/home/sheepyjb/ros/install/
/home/sheepyjb/ros/log/
```

其中最重要的是：

```text
install/
```

构建后必须执行：

```bash
source install/setup.bash
```

否则当前终端只认识系统 ROS 2，不认识你自己写的 `turtlesim_p_controller`。

## 这个包的最小理解路径

如果你刚开始学 ROS 2，建议按这个顺序读：

1. `package.xml`：先看这个包依赖什么。
2. `setup.py`：看 `ros2 run` 为什么能找到 `turtle_goal_controller`。
3. `turtle_goal_controller.py`：看节点如何订阅和发布。
4. `controller_math.py`：看速度命令怎么计算。
5. `test/test_controller_math.py`：看如何验证控制算法。

## 运行

终端 1：

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtlesim_node
```

终端 2：

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
colcon build --packages-select turtlesim_p_controller
source install/setup.bash
ros2 run turtlesim_p_controller turtle_goal_controller
```

调整目标点：

```bash
ros2 run turtlesim_p_controller turtle_goal_controller --ros-args \
  -p goal_x:=2.0 \
  -p goal_y:=9.0 \
  -p linear_gain:=1.0 \
  -p angular_gain:=3.0
```

## 单元测试

```bash
cd /home/sheepyjb/ros
PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test
```
