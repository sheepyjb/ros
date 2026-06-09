# 第 2 周第 1 小课：launch 文件与参数 YAML

这份文档对应第 2 周的第一小课：用 launch 文件一次启动多个节点，并把控制器参数从命令行迁移到 YAML 文件中管理。

本课目标：

```text
理解 launch 文件、参数 YAML、setup.py 安装数据文件之间的关系。
```

本课要学：

```text
ros2 launch
launch 文件
launch_ros.actions.Node
YAML 参数文件
setup.py 的 data_files
```

本课练习：

```text
用一个 launch 文件同时启动 turtlesim_node 和 turtle_goal_controller
用 YAML 文件集中管理 turtle_goal_controller 的参数
确认 launch/config 文件会被安装到 install/ 目录并能被 ROS 2 找到
```

先记住一句话：

```text
源码目录负责写文件，install/ 目录负责运行时让 ROS 2 找到文件。
```

## 一、为什么需要 launch 文件

第一周运行系统时需要开两个终端：

```bash
ros2 run turtlesim turtlesim_node
ros2 run turtlesim_p_controller turtle_goal_controller
```

这能帮助你理解节点和 topic，但项目一复杂就会很麻烦。

真实机器人系统通常需要同时启动：

- 机器人驱动节点
- 传感器节点
- 控制节点
- TF 节点
- RViz
- 参数文件

所以 ROS 2 用 launch 文件描述：

```text
启动哪些节点
每个节点叫什么
给节点加载哪些参数
输出日志放到哪里
```

本课新增的 launch 文件是：

```text
src/turtlesim_p_controller/launch/turtlesim_goal.launch.py
```

运行方式变成：

```bash
ros2 launch turtlesim_p_controller turtlesim_goal.launch.py
```

## 二、当前新增目录结构

第 2 周第 1 小课后，包里新增了这些文件：

```text
turtlesim_p_controller/
├── config/
│   └── goal_controller.yaml
├── launch/
│   └── turtlesim_goal.launch.py
├── test/
│   ├── test_controller_math.py
│   └── test_launch_assets.py
└── WEEK_02_01_LAUNCH_AND_PARAMS.md
```

它们分别负责：

- `launch/turtlesim_goal.launch.py`：描述一次启动哪些节点。
- `config/goal_controller.yaml`：保存控制器参数。
- `test/test_launch_assets.py`：确认 launch/config 文件存在，并且会被安装。
- `WEEK_02_01_LAUNCH_AND_PARAMS.md`：本课讲义。

## 三、launch 文件解释

源码：

```python
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_share = get_package_share_directory("turtlesim_p_controller")
    controller_params = os.path.join(package_share, "config", "goal_controller.yaml")

    return LaunchDescription(
        [
            Node(
                package="turtlesim",
                executable="turtlesim_node",
                name="turtlesim",
                output="screen",
            ),
            Node(
                package="turtlesim_p_controller",
                executable="turtle_goal_controller",
                name="turtle_goal_controller",
                parameters=[controller_params],
                output="screen",
            ),
        ]
    )
```

逐段理解：

```python
from launch import LaunchDescription
from launch_ros.actions import Node
```

`LaunchDescription` 是 launch 文件返回的启动描述。

`Node` 表示要启动一个 ROS 2 节点。

```python
package_share = get_package_share_directory("turtlesim_p_controller")
```

这行不是找源码目录，而是找安装后的 share 目录。

构建并 source 后，它大致对应：

```text
/home/sheepyjb/ros/install/turtlesim_p_controller/share/turtlesim_p_controller
```

```python
controller_params = os.path.join(package_share, "config", "goal_controller.yaml")
```

这行拼出参数文件路径。

也就是说，运行时真正被读取的是：

```text
install/turtlesim_p_controller/share/turtlesim_p_controller/config/goal_controller.yaml
```

不是源码目录里的：

```text
src/turtlesim_p_controller/config/goal_controller.yaml
```

这一点很重要。你修改源码目录里的 YAML 后，如果没有使用 symlink install，通常需要重新构建。

第一个 `Node`：

```python
Node(
    package="turtlesim",
    executable="turtlesim_node",
    name="turtlesim",
    output="screen",
)
```

意思是启动：

```bash
ros2 run turtlesim turtlesim_node
```

并把节点名设为：

```text
/turtlesim
```

第二个 `Node`：

```python
Node(
    package="turtlesim_p_controller",
    executable="turtle_goal_controller",
    name="turtle_goal_controller",
    parameters=[controller_params],
    output="screen",
)
```

意思是启动：

```bash
ros2 run turtlesim_p_controller turtle_goal_controller
```

并给它加载：

```text
config/goal_controller.yaml
```

## 四、YAML 参数文件解释

源码：

```yaml
turtle_goal_controller:
  ros__parameters:
    goal_x: 8.0
    goal_y: 8.0
    linear_gain: 1.2
    angular_gain: 4.0
    max_linear_speed: 2.0
    max_angular_speed: 4.0
    goal_tolerance: 0.15
```

最外层：

```yaml
turtle_goal_controller:
```

表示这些参数属于名为 `/turtle_goal_controller` 的节点。

中间层：

```yaml
ros__parameters:
```

这是 ROS 2 参数 YAML 的固定写法。注意是两个下划线：

```text
ros__parameters
```

下面每一项就是节点参数：

```yaml
goal_x: 8.0
goal_y: 8.0
linear_gain: 1.2
angular_gain: 4.0
max_linear_speed: 2.0
max_angular_speed: 4.0
goal_tolerance: 0.15
```

它们会覆盖 `turtle_goal_controller.py` 里声明的默认值。

如果 YAML 中没有写某个参数，节点就使用代码里的默认值。

## 五、setup.py 为什么也要改

只把文件放进 `launch/` 和 `config/` 还不够。

`ros2 launch` 查找的是安装后的 package share 目录，所以 `setup.py` 必须声明要安装这些文件。

当前关键配置：

```python
data_files=[
    ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
    (os.path.join("share", package_name), ["package.xml"]),
    (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
    (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
],
```

这四行分别安装：

- package 索引标记文件
- `package.xml`
- `launch/*.launch.py`
- `config/*.yaml`

如果少了 launch 安装声明，可能会出现：

```text
file 'turtlesim_goal.launch.py' was not found in the share directory
```

如果少了 config 安装声明，launch 文件能找到，但节点加载参数文件会失败。

## 六、package.xml 新增依赖

launch 文件中用到了：

```python
ament_index_python
launch
launch_ros
```

所以 `package.xml` 里新增：

```xml
<exec_depend>ament_index_python</exec_depend>
<exec_depend>launch</exec_depend>
<exec_depend>launch_ros</exec_depend>
```

`exec_depend` 表示运行时需要这些包。

## 七、构建和运行

每次新增 launch/config 这类需要安装的文件后，先重新构建：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select turtlesim_p_controller
source install/setup.bash
```

然后一条命令启动两个节点：

```bash
ros2 launch turtlesim_p_controller turtlesim_goal.launch.py
```

另开一个终端检查节点：

```bash
source /opt/ros/jazzy/setup.bash
source /home/sheepyjb/ros/install/setup.bash
ros2 node list
```

你应该看到类似：

```text
/turtle_goal_controller
/turtlesim
```

检查参数：

```bash
ros2 param get /turtle_goal_controller goal_x
ros2 param get /turtle_goal_controller linear_gain
```

你应该看到 YAML 里的值。

## 八、运行时修改参数

YAML 文件适合保存默认配置。

运行过程中，也可以临时改参数：

```bash
ros2 param set /turtle_goal_controller goal_x 2.0
ros2 param set /turtle_goal_controller goal_y 2.0
```

这会让目标点临时变成：

```text
(2.0, 2.0)
```

注意：

```text
ros2 param set 只影响当前正在运行的节点
修改 YAML 才会影响下一次 launch 的默认值
```

## 九、练习题

### 练习 1：用 launch 启动系统

运行：

```bash
ros2 launch turtlesim_p_controller turtlesim_goal.launch.py
```

观察：

- 是否打开 turtlesim 窗口
- 乌龟是否自动向目标点运动
- 终端里是否显示两个节点的日志

### 练习 2：确认节点列表

另开终端运行：

```bash
ros2 node list
```

写下你看到的节点名。

### 练习 3：确认参数来自 YAML

运行：

```bash
ros2 param get /turtle_goal_controller goal_x
ros2 param get /turtle_goal_controller angular_gain
```

观察返回值是否和 `config/goal_controller.yaml` 一致。

### 练习 4：修改 YAML 默认目标点

把 `config/goal_controller.yaml` 改成：

```yaml
goal_x: 2.0
goal_y: 8.0
```

然后重新构建并运行：

```bash
colcon build --packages-select turtlesim_p_controller
source install/setup.bash
ros2 launch turtlesim_p_controller turtlesim_goal.launch.py
```

观察乌龟是否朝新的目标点运动。

### 练习 5：运行中临时改目标点

launch 正在运行时，另开终端：

```bash
ros2 param set /turtle_goal_controller goal_x 9.0
ros2 param set /turtle_goal_controller goal_y 2.0
```

观察乌龟轨迹是否发生变化。

### 练习 6：读懂 launch 文件

打开：

```text
src/turtlesim_p_controller/launch/turtlesim_goal.launch.py
```

回答：

- 它启动了几个节点？
- 每个节点来自哪个 package？
- 哪个节点加载了参数 YAML？

### 练习 7：理解 setup.py 的 data_files

打开：

```text
src/turtlesim_p_controller/setup.py
```

回答：

- 哪一行安装 launch 文件？
- 哪一行安装 config 文件？
- 如果删掉 config 安装声明，会发生什么？

### 练习 8：运行测试

运行：

```bash
PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test
```

确认测试通过。

## 十、参考答案要点

### 练习 1

应该只用一条 `ros2 launch` 命令就能启动 turtlesim 和控制器节点。

### 练习 2

应该看到：

```text
/turtlesim
/turtle_goal_controller
```

### 练习 3

`goal_x` 应该是 `8.0`，`angular_gain` 应该是 `4.0`，除非你已经改过 YAML 或运行时参数。

### 练习 4

修改 YAML 后，要重新构建并重新 source，launch 才能读取安装后的新参数文件。

### 练习 5

`ros2 param set` 会立即影响当前运行的控制器，因为 `turtle_goal_controller.py` 每次收到位姿都会重新读取参数。

### 练习 6

launch 文件启动了两个节点：

- `turtlesim` 包里的 `turtlesim_node`
- `turtlesim_p_controller` 包里的 `turtle_goal_controller`

加载参数 YAML 的是：

```text
turtle_goal_controller
```

### 练习 7

安装 launch 文件的是：

```python
(os.path.join("share", package_name, "launch"), glob("launch/*.launch.py"))
```

安装 config 文件的是：

```python
(os.path.join("share", package_name, "config"), glob("config/*.yaml"))
```

如果删掉 config 安装声明，launch 文件中的参数路径会指向一个不存在的安装文件，控制器启动时可能无法加载参数。

### 练习 8

测试应该全部通过，说明：

- 控制数学仍然正确
- launch/config 文件存在
- `setup.py` 包含安装声明

## 十一、通过标准

完成本课后，你应该能做到：

- 解释 `ros2 run` 和 `ros2 launch` 的区别。
- 解释 launch 文件里的 `Node(package=..., executable=...)`。
- 用 YAML 文件给 ROS 2 节点加载参数。
- 知道 `ros__parameters` 是 ROS 2 参数 YAML 的固定字段。
- 知道 launch/config 文件需要通过 `setup.py` 安装。
- 能用一条 `ros2 launch` 命令启动 turtlesim 和控制器。

## 十二、本课总结

第一周你已经能手动启动节点并观察 topic。

第二周第一小课把这个系统组织得更像真实项目：

```text
launch 文件负责启动系统
YAML 文件负责管理参数
setup.py 负责把运行时需要的文件安装到 install/
```

这三个概念是后面 `robot_bringup`、URDF、RViz、Gazebo、Nav2 的基础。
