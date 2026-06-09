# 第 1 周：ROS 2 基础通信

这份文档对应学习计划里的第 1 周：ROS 2 基础通信。它按 0 基础入门来讲解 `/home/sheepyjb/ros/src/turtlesim_p_controller`，并配套练习题、观察问题和知识问答。

本周目标：

```text
理解 ROS 2 的节点、话题、服务、动作、参数，以及如何用命令行观察系统。
```

本周要学：

```text
ros2 node
ros2 topic
ros2 service
ros2 action
ros2 param
rqt_graph
turtlesim
```

本周练习：

```text
启动 turtlesim_node
写一个控制节点订阅 /turtle1/pose
发布 /turtle1/cmd_vel
用 P 控制让乌龟朝一个固定目标点运动
```

先记住三层关系：

```text
/home/sheepyjb/ros                  # workspace，工作空间
└── src/
    └── turtlesim_p_controller/     # package，功能包
        └── turtlesim_p_controller/ # Python 模块，真正放代码
```

ROS 2 项目通常不是一个文件，而是：

```text
workspace 管多个 package
package 里放节点、配置、测试和元信息
node 节点负责订阅、计算、发布
```

当前练习的目标是：

```text
读取乌龟位置 -> 计算速度 -> 发布速度 -> 让乌龟移动到目标点
```

## 一、整体目录结构

当前包的源码结构：

```text
turtlesim_p_controller/
├── README.md
├── WEEK_01_ROS2_BASIC_COMMUNICATION.md
├── package.xml
├── setup.py
├── setup.cfg
├── resource/
│   └── turtlesim_p_controller
├── test/
│   └── test_controller_math.py
└── turtlesim_p_controller/
    ├── __init__.py
    ├── controller_math.py
    └── turtle_goal_controller.py
```

你可能还会看到：

```text
__pycache__/
```

这是 Python 自动生成的缓存目录，不是你要学习的源码，不需要打开，也不需要提交到 git。

## 二、每个目录是什么

### 1. 外层 `turtlesim_p_controller/`

路径：

```text
/home/sheepyjb/ros/src/turtlesim_p_controller
```

这是一个 ROS 2 package 的根目录。

它里面放三类东西：

- ROS 2 包描述文件：`package.xml`
- Python 安装配置：`setup.py`、`setup.cfg`
- 源码、测试、文档：`turtlesim_p_controller/`、`test/`、`README.md`

你可以把它理解成：

```text
这个包的全部资料夹
```

### 2. `resource/`

路径：

```text
/home/sheepyjb/ros/src/turtlesim_p_controller/resource
```

这个目录给 ROS 2 的包索引系统用。

里面的文件：

```text
resource/turtlesim_p_controller
```

文件内容可以为空，但文件名很重要。它告诉 ROS 2：

```text
这里有一个 package 叫 turtlesim_p_controller
```

### 3. 内层 `turtlesim_p_controller/`

路径：

```text
/home/sheepyjb/ros/src/turtlesim_p_controller/turtlesim_p_controller
```

这是 Python 代码目录。

为什么和外层同名？

```text
外层 turtlesim_p_controller：ROS 2 package 名
内层 turtlesim_p_controller：Python import 模块名
```

Python 代码里写：

```python
from turtlesim_p_controller.controller_math import compute_velocity_command
```

这里的 `turtlesim_p_controller` 指的是内层 Python 模块目录。

### 4. `test/`

路径：

```text
/home/sheepyjb/ros/src/turtlesim_p_controller/test
```

这是测试目录。

当前只有一个测试文件：

```text
test_controller_math.py
```

它不打开 turtlesim 图形窗口，只测试控制数学是否正确。

## 三、每个文件是什么

### 1. `README.md`

这是人看的快速说明文档。

它告诉你：

- 这个 package 是什么
- 如何构建
- 如何运行 turtlesim
- 如何运行控制器
- 如何运行单元测试

它不参与程序运行。删掉它程序也能跑，但学习项目里应该保留。

### 2. `WEEK_01_ROS2_BASIC_COMMUNICATION.md`

就是你现在看的这份文档。

它用于从 0 基础理解目录、配置和代码。

它也不参与程序运行。

### 3. `package.xml`

这是 ROS 2 package 的身份证。

ROS 2 和 `colcon` 会读取它，知道：

- 包名
- 版本
- 描述
- 作者
- 许可证
- 依赖哪些 ROS 2 包
- 用什么构建系统

### 4. `setup.py`

这是 Python package 的安装说明。

`colcon build` 会读取它，把 Python 代码安装到 workspace 的 `install/` 目录里。

它还定义了 `ros2 run` 能运行的命令。

### 5. `setup.cfg`

这是 Python 安装路径配置。

它让可执行脚本安装到 ROS 2 习惯的位置：

```text
install/turtlesim_p_controller/lib/turtlesim_p_controller/
```

### 6. `resource/turtlesim_p_controller`

这是一个空的标记文件。

它的作用不是写代码，而是让 ROS 2 的 package index 能发现这个包。

### 7. `turtlesim_p_controller/__init__.py`

这是 Python 包标记文件。

有了它，Python 才能把这个目录当成可导入模块。

### 8. `turtlesim_p_controller/controller_math.py`

这是控制算法文件。

它不直接使用 ROS 2，只做数学计算：

```text
当前位姿 + 目标点 + 控制参数 -> 速度命令
```

这种拆法很重要。算法和 ROS 通信分开，代码更容易看，也更容易测试。

### 9. `turtlesim_p_controller/turtle_goal_controller.py`

这是 ROS 2 节点文件。

它负责：

- 创建节点
- 声明参数
- 订阅 `/turtle1/pose`
- 发布 `/turtle1/cmd_vel`
- 调用控制算法

### 10. `test/test_controller_math.py`

这是测试文件。

它负责验证：

- 角度计算对不对
- 速度方向对不对
- 到达目标附近是否停止

## 四、`package.xml` 逐行解释

源码：

```xml
<?xml version="1.0"?>
<package format="3">
  <name>turtlesim_p_controller</name>
  <version>0.1.0</version>
  <description>ROS 2 turtlesim P 控制学习练习。</description>
  <maintainer email="student@example.com">ROS 2 Learner</maintainer>
  <license>MIT</license>

  <depend>geometry_msgs</depend>
  <depend>rclpy</depend>
  <depend>turtlesim</depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

逐行说明：

- 第 1 行：声明这是 XML 文件。
- 第 2 行：开始定义一个 ROS 2 package，`format="3"` 是 ROS 2 常用格式。
- 第 3 行：包名是 `turtlesim_p_controller`。运行时会用到这个名字。
- 第 4 行：包版本是 `0.1.0`。
- 第 5 行：一句话说明这个包做什么。
- 第 6 行：维护者信息。现在是学习项目，所以用了占位邮箱。
- 第 7 行：许可证。这里写 MIT。
- 第 9 行：依赖 `geometry_msgs`，因为要发布 `Twist` 速度消息。
- 第 10 行：依赖 `rclpy`，因为节点是用 Python 写的。
- 第 11 行：依赖 `turtlesim`，因为要订阅 `turtlesim.msg.Pose`，也要和 turtlesim 示例配合。
- 第 13 行：测试相关依赖，给 ROS 2 lint 测试使用。
- 第 14 行：同上，测试相关依赖。
- 第 16 行：开始写导出信息。
- 第 17 行：声明这个包用 `ament_python` 构建。
- 第 18 行：结束导出信息。
- 第 19 行：结束 package 定义。

最关键的是这三处：

```xml
<name>turtlesim_p_controller</name>
<depend>rclpy</depend>
<build_type>ament_python</build_type>
```

它们分别说明：

```text
包叫什么
需要 ROS 2 Python 客户端
这是 Python 类型的 ROS 2 包
```

## 五、`setup.py` 逐行解释

源码：

```python
from setuptools import setup


package_name = "turtlesim_p_controller"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="ROS 2 Learner",
    maintainer_email="student@example.com",
    description="ROS 2 turtlesim P 控制学习练习。",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "turtle_goal_controller = turtlesim_p_controller.turtle_goal_controller:main",
        ],
    },
)
```

逐行说明：

- 第 1 行：从 `setuptools` 导入 `setup`。这是 Python 打包工具。
- 第 4 行：把包名保存到变量 `package_name`。后面重复用这个名字，避免写错。
- 第 6 行：调用 `setup()`，开始描述这个 Python 包怎么安装。
- 第 7 行：安装后的包名使用 `package_name`。
- 第 8 行：版本号。
- 第 9 行：声明要安装的 Python 模块是 `turtlesim_p_controller`。
- 第 10 行：开始声明额外要安装的数据文件。
- 第 11 行：安装 `resource/turtlesim_p_controller`，让 ROS 2 package index 能发现这个包。
- 第 12 行：安装 `package.xml`，让 ROS 2 能读取包元信息。
- 第 13 行：结束 `data_files`。
- 第 14 行：安装这个包需要 `setuptools`。
- 第 15 行：`zip_safe=True` 表示可以按 zip 安装。这里保持默认即可，不是入门重点。
- 第 16 行：维护者名字。
- 第 17 行：维护者邮箱。
- 第 18 行：包描述。
- 第 19 行：许可证。
- 第 20 行：测试依赖。当前实际测试用的是 Python 标准库 `unittest`，这里保留 ROS 2 模板常见写法。
- 第 21 行：开始声明命令行入口。
- 第 22 行：`console_scripts` 表示生成一个终端可执行命令。
- 第 23 行：定义命令名和它对应的 Python 函数。
- 第 24 行：结束命令列表。
- 第 25 行：结束 `entry_points`。
- 第 26 行：结束 `setup()`。

第 23 行最重要：

```python
"turtle_goal_controller = turtlesim_p_controller.turtle_goal_controller:main"
```

它的意思是：

```text
终端命令 turtle_goal_controller
会调用
turtlesim_p_controller/turtle_goal_controller.py 里的 main 函数
```

所以你能运行：

```bash
ros2 run turtlesim_p_controller turtle_goal_controller
```

## 六、`setup.cfg` 逐行解释

源码：

```ini
[develop]
script_dir=$base/lib/turtlesim_p_controller
[install]
install_scripts=$base/lib/turtlesim_p_controller
```

逐行说明：

- 第 1 行：`[develop]` 是开发模式安装配置。
- 第 2 行：开发模式下，把脚本放到 `$base/lib/turtlesim_p_controller`。
- 第 3 行：`[install]` 是正常安装配置。
- 第 4 行：正常安装时，也把脚本放到 `$base/lib/turtlesim_p_controller`。

为什么要这样？

ROS 2 查找可执行文件时，会到 package 对应的 `lib/<package_name>/` 目录下找。

也就是类似：

```text
install/turtlesim_p_controller/lib/turtlesim_p_controller/turtle_goal_controller
```

## 七、`resource/turtlesim_p_controller` 解释

这个文件是空文件。

它的重点不是内容，而是路径和文件名：

```text
resource/turtlesim_p_controller
```

`setup.py` 会把它安装到：

```text
share/ament_index/resource_index/packages/
```

ROS 2 通过这个索引知道：

```text
turtlesim_p_controller 这个包存在
```

如果没有它，包可能构建了，但 ROS 2 不一定能正确发现它。

## 八、`__init__.py` 解释

源码：

```python
"""turtlesim P 控制练习包。"""
```

这个文件只有一行字符串说明。

它的核心作用是告诉 Python：

```text
这个目录是一个 Python package
```

有了它，Python 才能这样导入：

```python
from turtlesim_p_controller.controller_math import compute_velocity_command
```

如果你刚开始学，可以先记住：

```text
Python 源码目录里通常需要 __init__.py
```

## 九、`controller_math.py` 逐代码解释

这个文件只负责控制算法，不负责 ROS 2 通信。

源码：

```python
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ControllerConfig:
    goal_x: float
    goal_y: float
    linear_gain: float
    angular_gain: float
    max_linear_speed: float
    max_angular_speed: float
    goal_tolerance: float


@dataclass(frozen=True)
class TurtlePose:
    x: float
    y: float
    theta: float


@dataclass(frozen=True)
class VelocityCommand:
    linear_x: float
    angular_z: float


def normalize_angle(angle: float) -> float:
    two_pi = 2.0 * math.pi
    while angle > math.pi:
        angle -= two_pi
    while angle < -math.pi:
        angle += two_pi
    return angle


def _clamp(value: float, limit: float) -> float:
    return max(-limit, min(limit, value))


def compute_velocity_command(
    pose: TurtlePose,
    config: ControllerConfig,
) -> VelocityCommand:
    dx = config.goal_x - pose.x
    dy = config.goal_y - pose.y
    distance_error = math.hypot(dx, dy)
    if distance_error < config.goal_tolerance:
        return VelocityCommand(linear_x=0.0, angular_z=0.0)

    target_angle = math.atan2(dy, dx)
    angle_error = normalize_angle(target_angle - pose.theta)
    linear_x = min(config.max_linear_speed, config.linear_gain * distance_error)
    angular_z = _clamp(config.angular_gain * angle_error, config.max_angular_speed)
    return VelocityCommand(linear_x=linear_x, angular_z=angular_z)
```

逐行说明：

- 第 1 行：导入 Python 数学库 `math`。后面要用 `pi`、`hypot`、`atan2`。
- 第 2 行：导入 `dataclass`。它可以快速定义只存数据的类。
- 第 5 行：`@dataclass(frozen=True)` 表示下面这个类是数据类，并且创建后不建议修改。
- 第 6 行：定义 `ControllerConfig`，意思是“控制器配置”。
- 第 7 行：`goal_x`，目标点的 x 坐标。
- 第 8 行：`goal_y`，目标点的 y 坐标。
- 第 9 行：`linear_gain`，线速度比例系数。距离误差越大，速度越大。
- 第 10 行：`angular_gain`，角速度比例系数。角度误差越大，转得越快。
- 第 11 行：`max_linear_speed`，最大线速度，防止跑太快。
- 第 12 行：`max_angular_speed`，最大角速度，防止转太快。
- 第 13 行：`goal_tolerance`，到目标多近算到达。
- 第 16 行：定义 `TurtlePose`，意思是“乌龟当前位姿”。
- 第 18 行：当前 x 坐标。
- 第 19 行：当前 y 坐标。
- 第 20 行：当前朝向角 `theta`。
- 第 23 行：定义 `VelocityCommand`，意思是“速度命令”。
- 第 25 行：`linear_x`，前进速度。
- 第 26 行：`angular_z`，绕 z 轴旋转速度，也就是左转或右转速度。
- 第 29 行：定义 `normalize_angle` 函数，用于把角度限制在 `[-pi, pi]` 附近。
- 第 30 行：计算 `2*pi`，也就是一整圈。
- 第 31 行：如果角度大于 `pi`，说明角度太大。
- 第 32 行：减去一整圈，让角度回到合理范围。
- 第 33 行：如果角度小于 `-pi`，说明角度太小。
- 第 34 行：加上一整圈，让角度回到合理范围。
- 第 35 行：返回归一化后的角度。
- 第 38 行：定义 `_clamp` 函数，用于限幅。函数名前面的 `_` 表示“内部使用”。
- 第 39 行：把 `value` 限制在 `[-limit, limit]` 之间。
- 第 42 行：定义核心函数 `compute_velocity_command`。
- 第 43 行：第一个参数是当前位姿 `pose`。
- 第 44 行：第二个参数是控制配置 `config`。
- 第 45 行：返回值是 `VelocityCommand`。
- 第 46 行：计算目标点和当前位置的 x 方向差值。
- 第 47 行：计算目标点和当前位置的 y 方向差值。
- 第 48 行：用勾股定理计算距离误差。
- 第 49 行：如果距离已经小于容许误差。
- 第 50 行：返回 0 速度，让乌龟停止。
- 第 52 行：计算从当前位置指向目标点的角度。
- 第 53 行：计算目标角度和当前朝向之间的误差，并归一化。
- 第 54 行：根据距离误差算线速度，同时不超过最大线速度。
- 第 55 行：根据角度误差算角速度，同时不超过最大角速度。
- 第 56 行：返回最终速度命令。

这一段是整个控制器的核心：

```python
dx = config.goal_x - pose.x
dy = config.goal_y - pose.y
distance_error = math.hypot(dx, dy)
target_angle = math.atan2(dy, dx)
angle_error = normalize_angle(target_angle - pose.theta)
```

意思是：

```text
先算目标在哪
再算离目标多远
再算应该朝哪个方向
再算当前方向和目标方向差多少
```

控制律是：

```python
linear_x = min(config.max_linear_speed, config.linear_gain * distance_error)
angular_z = _clamp(config.angular_gain * angle_error, config.max_angular_speed)
```

对应控制理论里的 P 控制：

```text
输出 = 比例系数 * 误差
```

## 十、`turtle_goal_controller.py` 逐代码解释

这个文件负责 ROS 2 通信。

源码：

```python
import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from turtlesim.msg import Pose

from turtlesim_p_controller.controller_math import (
    ControllerConfig,
    TurtlePose,
    compute_velocity_command,
)


class TurtleGoalController(Node):
    def __init__(self):
        super().__init__("turtle_goal_controller")
        self.declare_parameter("goal_x", 8.0)
        self.declare_parameter("goal_y", 8.0)
        self.declare_parameter("linear_gain", 1.2)
        self.declare_parameter("angular_gain", 4.0)
        self.declare_parameter("max_linear_speed", 2.0)
        self.declare_parameter("max_angular_speed", 4.0)
        self.declare_parameter("goal_tolerance", 0.15)

        self._cmd_vel_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.create_subscription(Pose, "/turtle1/pose", self._on_pose, 10)

    def _on_pose(self, msg: Pose) -> None:
        config = self._read_config()
        pose = TurtlePose(x=msg.x, y=msg.y, theta=msg.theta)
        command = compute_velocity_command(pose, config)

        twist = Twist()
        twist.linear.x = command.linear_x
        twist.angular.z = command.angular_z
        self._cmd_vel_pub.publish(twist)

    def _read_config(self) -> ControllerConfig:
        return ControllerConfig(
            goal_x=self.get_parameter("goal_x").value,
            goal_y=self.get_parameter("goal_y").value,
            linear_gain=self.get_parameter("linear_gain").value,
            angular_gain=self.get_parameter("angular_gain").value,
            max_linear_speed=self.get_parameter("max_linear_speed").value,
            max_angular_speed=self.get_parameter("max_angular_speed").value,
            goal_tolerance=self.get_parameter("goal_tolerance").value,
        )


def main(args=None):
    rclpy.init(args=args)
    node = TurtleGoalController()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
```

逐行说明：

- 第 1 行：导入 `rclpy`，这是 ROS 2 的 Python 客户端库。
- 第 2 行：导入 `Twist` 消息。`Twist` 用来表示速度。
- 第 3 行：导入 `Node`，所有 ROS 2 Python 节点都要继承它。
- 第 4 行：导入 turtlesim 的 `Pose` 消息，表示乌龟位置和朝向。
- 第 6 到 10 行：从自己的算法文件中导入配置、位姿和计算函数。
- 第 13 行：定义 `TurtleGoalController` 类，它继承 `Node`，所以它是一个 ROS 2 节点。
- 第 14 行：定义初始化函数。创建对象时自动执行。
- 第 15 行：调用父类初始化，并把节点名设为 `turtle_goal_controller`。
- 第 16 行：声明参数 `goal_x`，默认值是 `8.0`。
- 第 17 行：声明参数 `goal_y`，默认值是 `8.0`。
- 第 18 行：声明线速度比例系数。
- 第 19 行：声明角速度比例系数。
- 第 20 行：声明最大线速度。
- 第 21 行：声明最大角速度。
- 第 22 行：声明目标容许误差。
- 第 24 行：创建发布者，向 `/turtle1/cmd_vel` 发布 `Twist` 消息，队列长度是 10。
- 第 25 行：创建订阅者，订阅 `/turtle1/pose`，收到消息后调用 `self._on_pose`。
- 第 27 行：定义回调函数 `_on_pose`。每收到一次位姿消息，这个函数就执行一次。
- 第 28 行：读取当前参数。
- 第 29 行：把 ROS 2 的 `Pose` 消息转换成我们自己的 `TurtlePose` 数据类。
- 第 30 行：调用控制算法，计算速度命令。
- 第 32 行：创建一个 ROS 2 `Twist` 消息。
- 第 33 行：设置前进速度。
- 第 34 行：设置旋转速度。
- 第 35 行：发布速度消息，让 turtlesim 执行运动。
- 第 37 行：定义 `_read_config` 函数，用于读取参数。
- 第 38 行：返回一个 `ControllerConfig` 对象。
- 第 39 到 45 行：从 ROS 2 参数系统读取每个参数的当前值。
- 第 49 行：定义 `main` 函数。`ros2 run` 最终会调用它。
- 第 50 行：初始化 ROS 2 Python 环境。
- 第 51 行：创建节点对象。
- 第 52 行：开始 `try`，用于保证退出时能清理资源。
- 第 53 行：`rclpy.spin(node)` 让节点持续运行，等待话题消息。
- 第 54 行：无论正常退出还是 Ctrl+C，都进入清理逻辑。
- 第 55 行：销毁节点。
- 第 56 行：关闭 ROS 2 Python 环境。
- 第 59 行：如果直接用 Python 运行这个文件。
- 第 60 行：调用 `main()`。

最重要的数据流是：

```python
self.create_subscription(Pose, "/turtle1/pose", self._on_pose, 10)
```

意思是：

```text
只要 /turtle1/pose 有新消息，就调用 _on_pose
```

然后 `_on_pose` 里：

```python
command = compute_velocity_command(pose, config)
self._cmd_vel_pub.publish(twist)
```

意思是：

```text
根据当前位置算速度，再把速度发出去
```

## 十一、`test/test_controller_math.py` 逐代码解释

这个文件负责测试控制算法。

源码：

```python
import math
import unittest

from turtlesim_p_controller.controller_math import (
    ControllerConfig,
    TurtlePose,
    compute_velocity_command,
    normalize_angle,
)


class ControllerMathTest(unittest.TestCase):
    def test_normalize_angle_wraps_to_pi_range(self):
        self.assertAlmostEqual(normalize_angle(3 * math.pi), math.pi)
        self.assertAlmostEqual(normalize_angle(-3 * math.pi), -math.pi)
        self.assertAlmostEqual(normalize_angle(0.5), 0.5)

    def test_compute_velocity_command_moves_toward_goal(self):
        config = ControllerConfig(
            goal_x=8.0,
            goal_y=5.5,
            linear_gain=1.0,
            angular_gain=2.0,
            max_linear_speed=2.0,
            max_angular_speed=3.0,
            goal_tolerance=0.15,
        )
        pose = TurtlePose(x=5.5, y=5.5, theta=0.0)

        command = compute_velocity_command(pose, config)

        self.assertGreater(command.linear_x, 0.0)
        self.assertAlmostEqual(command.angular_z, 0.0)
        self.assertLessEqual(command.linear_x, config.max_linear_speed)

    def test_compute_velocity_command_turns_shortest_direction(self):
        config = ControllerConfig(
            goal_x=5.5,
            goal_y=8.0,
            linear_gain=1.0,
            angular_gain=2.0,
            max_linear_speed=2.0,
            max_angular_speed=3.0,
            goal_tolerance=0.15,
        )
        pose = TurtlePose(x=5.5, y=5.5, theta=0.0)

        command = compute_velocity_command(pose, config)

        self.assertGreater(command.angular_z, 0.0)
        self.assertLessEqual(abs(command.angular_z), config.max_angular_speed)

    def test_compute_velocity_command_stops_inside_tolerance(self):
        config = ControllerConfig(
            goal_x=5.55,
            goal_y=5.5,
            linear_gain=1.0,
            angular_gain=2.0,
            max_linear_speed=2.0,
            max_angular_speed=3.0,
            goal_tolerance=0.15,
        )
        pose = TurtlePose(x=5.5, y=5.5, theta=0.0)

        command = compute_velocity_command(pose, config)

        self.assertEqual(command.linear_x, 0.0)
        self.assertEqual(command.angular_z, 0.0)


if __name__ == "__main__":
    unittest.main()
```

逐行说明：

- 第 1 行：导入数学库，测试里要用 `math.pi`。
- 第 2 行：导入 Python 标准测试库 `unittest`。
- 第 4 到 9 行：从控制算法文件里导入要测试的类和函数。
- 第 12 行：定义测试类，继承 `unittest.TestCase`。
- 第 13 行：第一个测试，验证角度归一化。
- 第 14 行：`3*pi` 应该被归一化成 `pi`。
- 第 15 行：`-3*pi` 应该被归一化成 `-pi`。
- 第 16 行：`0.5` 本来就在范围内，应保持不变。
- 第 18 行：第二个测试，验证目标在正前方时会前进。
- 第 19 到 27 行：构造控制参数。
- 第 28 行：构造当前位姿。乌龟在 `(5.5, 5.5)`，朝向 0。
- 第 30 行：调用控制算法。
- 第 32 行：断言线速度大于 0，说明会往前走。
- 第 33 行：断言角速度接近 0，说明目标就在正前方，不需要转弯。
- 第 34 行：断言线速度没有超过最大速度。
- 第 36 行：第三个测试，验证目标在左上方时会左转。
- 第 37 到 45 行：构造目标在 `(5.5, 8.0)` 的控制参数。
- 第 46 行：当前位置还是 `(5.5, 5.5)`，朝向 0。
- 第 48 行：调用控制算法。
- 第 50 行：断言角速度大于 0，说明向左转。
- 第 51 行：断言角速度没有超过最大角速度。
- 第 53 行：第四个测试，验证接近目标点时停止。
- 第 54 到 62 行：目标点设得离当前位置非常近。
- 第 63 行：当前位置是 `(5.5, 5.5)`。
- 第 65 行：调用控制算法。
- 第 67 行：断言线速度为 0。
- 第 68 行：断言角速度为 0。
- 第 71 行：如果直接运行这个测试文件。
- 第 72 行：启动 unittest 测试。

运行测试：

```bash
cd /home/sheepyjb/ros
PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test
```

如果看到：

```text
OK
```

说明算法测试通过。

## 十二、整体运行流程

从你输入命令开始，整个系统发生了这些事：

### 1. 加载系统 ROS 2

```bash
source /opt/ros/jazzy/setup.bash
```

作用：

```text
让终端认识 ros2、rclpy、turtlesim 等系统包
```

### 2. 构建自己的 package

```bash
cd /home/sheepyjb/ros
colcon build --packages-select turtlesim_p_controller
```

作用：

```text
读取 package.xml、setup.py、setup.cfg
把自己的包安装到 install/
```

### 3. 加载自己的 workspace

```bash
source install/setup.bash
```

作用：

```text
让终端认识你自己写的 turtlesim_p_controller
```

### 4. 启动 turtlesim

```bash
ros2 run turtlesim turtlesim_node
```

启动官方 turtlesim 节点。

它会：

```text
发布 /turtle1/pose
订阅 /turtle1/cmd_vel
```

### 5. 启动自己的控制器

```bash
ros2 run turtlesim_p_controller turtle_goal_controller
```

启动你写的节点。

它会：

```text
订阅 /turtle1/pose
发布 /turtle1/cmd_vel
```

### 6. 两个节点通过 topic 连接

最终关系：

```text
turtlesim_node
  /turtle1/pose
        ↓
turtle_goal_controller
  compute_velocity_command()
        ↓
  /turtle1/cmd_vel
        ↓
turtlesim_node
```

这就是 ROS 2 最基本的闭环控制结构。

## 十三、你应该按什么顺序理解

建议按这个顺序看：

1. 先看目录结构，知道哪些是配置，哪些是代码。
2. 看 `package.xml`，理解依赖。
3. 看 `setup.py`，理解 `ros2 run` 怎么找到程序。
4. 看 `turtle_goal_controller.py`，理解 ROS 2 节点如何收发消息。
5. 看 `controller_math.py`，理解控制算法。
6. 看 `test/test_controller_math.py`，理解怎么验证算法。

先不要急着学 Gazebo、Nav2、YOLO 接入。当前阶段最重要的是把这四个概念吃透：

```text
package
node
topic
message
```

## 十四、第一周练习题

这一节用来检查你是不是真的掌握了第一周内容。不要只复制命令，要边做边观察输出。

### 练习 1：启动 turtlesim

目标：确认你能启动第一个 ROS 2 节点。

终端 1：

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtlesim_node
```

观察：

- 是否弹出 TurtleSim 窗口。
- 终端里是否出现 `Starting turtlesim`。
- 是否生成了一只 `turtle1`。

问题：

1. 这条命令启动了哪个 package 里的哪个可执行程序？
2. 这个节点的节点名是什么？
3. 这个终端为什么不能关？

验收标准：

- 你能解释 `ros2 run turtlesim turtlesim_node` 里的两个 `turtlesim` 分别是什么。
- 你能说出这个节点负责仿真乌龟，并提供 `/turtle1/pose`、`/turtle1/cmd_vel` 等接口。

### 练习 2：查看节点

目标：掌握 `ros2 node`。

另开终端：

```bash
source /opt/ros/jazzy/setup.bash
ros2 node list
```

继续查看节点详情：

```bash
ros2 node info /turtlesim
```

问题：

1. `ros2 node list` 输出了什么？
2. `/turtlesim` 有哪些 publishers？
3. `/turtlesim` 有哪些 subscribers？
4. `/turtlesim` 提供了哪些 services？
5. `/turtlesim` 提供了哪个 action？

验收标准：

- 你能从 `ros2 node info /turtlesim` 里找到 `/turtle1/pose`。
- 你能从 `ros2 node info /turtlesim` 里找到 `/turtle1/cmd_vel`。
- 你能说出 publisher 是“发布者”，subscriber 是“订阅者”。

### 练习 3：查看话题

目标：理解 topic 是连续数据流。

执行：

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic list
```

查看位姿数据：

```bash
ros2 topic echo /turtle1/pose
```

查看话题频率：

```bash
ros2 topic hz /turtle1/pose
```

问题：

1. `/turtle1/pose` 是谁发布的？
2. `/turtle1/pose` 的消息类型是什么？
3. `x`、`y`、`theta` 分别表示什么？
4. 为什么 `/turtle1/pose` 适合用 topic，而不是 service？

验收标准：

- 你能解释 `/turtle1/pose` 是 turtlesim 持续发布的当前状态。
- 你能看懂 `x`、`y`、`theta`。
- 你能说出 topic 适合传连续变化的数据。

### 练习 4：手动发布速度

目标：理解 `/turtle1/cmd_vel` 的方向。

执行一次速度命令：

```bash
source /opt/ros/jazzy/setup.bash
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 1.0}, angular: {z: 0.0}}"
```

再试一个转弯命令：

```bash
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 1.0}, angular: {z: 1.0}}"
```

问题：

1. `/turtle1/cmd_vel` 是谁订阅的？
2. `linear.x` 控制什么？
3. `angular.z` 控制什么？
4. 为什么这里的消息类型是 `geometry_msgs/msg/Twist`？

验收标准：

- 你能通过手动发布 `/turtle1/cmd_vel` 让乌龟动起来。
- 你能说清楚 `/turtle1/cmd_vel` 是“控制器发给 turtlesim 的速度命令”。

### 练习 5：运行自己的 P 控制器

目标：理解自己写的节点如何接入 ROS 图。

终端 1 保持 turtlesim 运行。

终端 2：

```bash
cd /home/sheepyjb/ros
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run turtlesim_p_controller turtle_goal_controller
```

观察：

- 乌龟是否朝目标点移动。
- 是否到目标点附近后停止。

另开终端查看节点：

```bash
source /opt/ros/jazzy/setup.bash
source /home/sheepyjb/ros/install/setup.bash
ros2 node list
```

问题：

1. 自己写的节点名是什么？
2. 它订阅哪个 topic？
3. 它发布哪个 topic？
4. 它为什么需要同时读位姿和发速度？

验收标准：

- 你能看到 `/turtle_goal_controller`。
- 你能解释闭环关系：读 `/turtle1/pose`，算速度，发 `/turtle1/cmd_vel`。

### 练习 6：调节 P 控制参数

目标：观察 `linear_gain` 和 `angular_gain` 的影响。

先停掉旧控制器，然后运行：

```bash
cd /home/sheepyjb/ros
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run turtlesim_p_controller turtle_goal_controller --ros-args \
  -p goal_x:=9.0 \
  -p goal_y:=9.0 \
  -p linear_gain:=0.4 \
  -p angular_gain:=6.0
```

再试一组：

```bash
ros2 run turtlesim_p_controller turtle_goal_controller --ros-args \
  -p goal_x:=9.0 \
  -p goal_y:=9.0 \
  -p linear_gain:=1.5 \
  -p angular_gain:=1.0
```

问题：

1. `linear_gain` 变大时，乌龟前进更快还是更慢？
2. `angular_gain` 变小时，为什么可能绕圈？
3. 为什么 `linear_gain:=8` 会报类型错误，而 `linear_gain:=8.0` 可以？
4. 如果乌龟已经到目标附近，再调参数为什么可能看不出效果？

验收标准：

- 你能观察到不同参数导致不同轨迹。
- 你能解释“角速度系数太小会转向不足，线速度还在前进，所以可能绕圈”。

### 练习 7：使用 service 重置实验

目标：理解 service 是一次请求一次响应。

保持 turtlesim 运行，另开终端：

```bash
source /opt/ros/jazzy/setup.bash
ros2 service list
```

调用 reset：

```bash
ros2 service call /reset std_srvs/srv/Empty "{}"
```

问题：

1. `/reset` 是谁提供的？
2. `ros2 service call` 和 `ros2 topic pub` 有什么不同？
3. 如果 turtlesim 没有运行，调用 `/reset` 会发生什么？
4. 为什么比较不同参数时，最好 reset 到同一起点？

验收标准：

- 你能成功 reset turtlesim。
- 你能解释 service 适合“一次性请求”，例如重置仿真。

### 练习 8：查看 action

目标：初步认识 action 适合长时间任务。

执行：

```bash
source /opt/ros/jazzy/setup.bash
ros2 action list
```

查看 action 信息：

```bash
ros2 action info /turtle1/rotate_absolute
```

如果你想试一下，先停掉自己的控制器，再执行：

```bash
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 1.57}"
```

问题：

1. turtlesim 提供了哪个 action？
2. action 和 service 有什么区别？
3. 为什么“旋转到某个角度”适合用 action？

验收标准：

- 你能说出 action 适合有持续过程、可反馈、可取消的任务。
- 你知道 service 更适合短的一问一答。

### 练习 9：用 rqt_graph 看系统结构

目标：把节点和话题关系可视化。

执行：

```bash
source /opt/ros/jazzy/setup.bash
rqt_graph
```

问题：

1. 图里有哪些节点？
2. `/turtle1/pose` 的箭头从哪里指向哪里？
3. `/turtle1/cmd_vel` 的箭头从哪里指向哪里？
4. 为什么 rqt_graph 对调试 ROS 系统很有用？

验收标准：

- 你能在图中看出 turtlesim 和控制器之间的通信方向。
- 你能用图解释闭环控制结构。

### 练习 10：排查常见错误

目标：遇到问题时能按顺序定位。

故意新开一个终端，只执行：

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim_p_controller turtle_goal_controller
```

如果出现：

```text
Package 'turtlesim_p_controller' not found
```

问题：

1. 少执行了哪条命令？
2. `/opt/ros/jazzy/setup.bash` 和 `install/setup.bash` 分别负责什么？
3. 如果 `/reset` 一直显示 `waiting for service to become available...`，你应该先检查什么？

验收标准：

- 你能主动补上 `source /home/sheepyjb/ros/install/setup.bash`。
- 你能按“节点 -> 话题/服务 -> 参数 -> 环境 source”的顺序排查。

## 十五、知识问答

这些问题不要求背诵，但要能用自己的话讲清楚。

1. ROS 2 workspace 是什么？
2. ROS 2 package 是什么？
3. node 是什么？
4. topic 是什么？
5. service 是什么？
6. action 是什么？
7. parameter 是什么？
8. `/turtle1/pose` 的消息方向是什么？
9. `/turtle1/cmd_vel` 的消息方向是什么？
10. 为什么控制器要订阅 `/turtle1/pose`？
11. 为什么控制器要发布 `/turtle1/cmd_vel`？
12. 什么是闭环控制？
13. 为什么角速度要根据角度误差计算？
14. 为什么 `angular_gain` 太小可能导致绕圈？
15. 为什么到目标附近后速度变成 0？
16. 为什么 `linear_gain:=8` 会类型错误？
17. 为什么每次新终端都要 source 环境？
18. `ros2 node list` 用来查什么？
19. `ros2 topic echo` 用来查什么？
20. `rqt_graph` 比命令行好在哪里？

## 十六、参考答案要点

1. workspace 是工作空间，里面通常有 `src/`、`build/`、`install/`、`log/`。
2. package 是功能包，一个 package 负责一类功能。
3. node 是运行中的功能单元，例如 `/turtlesim`、`/turtle_goal_controller`。
4. topic 是连续数据流，适合位姿、速度、图像、雷达这类不断变化的数据。
5. service 是一次请求一次响应，适合 reset、查询、保存地图这类短操作。
6. action 是有过程的任务，适合导航、旋转到角度、机械臂运动这类可反馈任务。
7. parameter 是节点运行配置，例如目标点、速度比例系数。
8. `/turtlesim` 发布 `/turtle1/pose`，控制器订阅它。
9. 控制器发布 `/turtle1/cmd_vel`，`/turtlesim` 订阅它。
10. 控制器需要知道当前位置，才能计算离目标还有多远、方向差多少。
11. 控制器需要发速度，才能让 turtlesim 里的乌龟运动。
12. 闭环控制是“测量当前状态 -> 计算误差 -> 输出控制量 -> 状态改变 -> 再测量”。
13. 角速度根据角度误差计算，才能偏得多时快转，偏得少时慢转，对准后不转。
14. `angular_gain` 太小时转向修正慢，但线速度还在前进，所以可能绕大圈。
15. 因为 `distance_error < goal_tolerance` 时，代码主动返回 0 速度。
16. ROS 2 参数有类型；`8` 是整数，`8.0` 是浮点数，而代码声明的默认值是浮点数。
17. `source /opt/ros/jazzy/setup.bash` 让终端认识系统 ROS 2；`source install/setup.bash` 让终端认识自己的 workspace。
18. `ros2 node list` 用来查看当前有哪些节点正在运行。
19. `ros2 topic echo` 用来查看某个 topic 上正在传输的消息内容。
20. `rqt_graph` 能把节点和 topic 的关系画成图，更容易看清系统结构。

## 十七、第一周通过标准

你可以进入下一周的标准：

- 能独立启动 `turtlesim_node`。
- 能独立启动 `turtle_goal_controller`。
- 能解释 `/turtle1/pose` 和 `/turtle1/cmd_vel` 的方向。
- 能用 `ros2 node list`、`ros2 topic list`、`ros2 topic echo` 观察系统。
- 能用 `/reset` 服务重置 turtlesim。
- 能说出 service 和 topic 的区别。
- 能找到 turtlesim 的 action，并说出 action 和 service 的区别。
- 能调节 `linear_gain` 和 `angular_gain`，并解释轨迹变化。
- 能说明为什么角速度要根据角度误差闭环控制。
- 遇到 `Package not found`、参数类型错误、`/reset` 等待服务时，能按顺序排查。
