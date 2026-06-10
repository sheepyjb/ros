# 第 2 周第 2 小课：robot_bringup 包与工作空间组织

这份文档对应第 2 周第 2 小课：创建 `robot_bringup` 包，并理解 ROS 2 workspace 中多个 package 的分工。

本课目标：

```text
理解功能包、启动编排包、工作空间目录之间的关系。
```

本课要学：

```text
robot_bringup
功能包和 bringup 包
src/build/install/log
ament_python 包结构
跨 package 启动节点
```

本课练习：

```text
创建 robot_bringup 包
把统一启动入口放到 robot_bringup/launch/
用 ros2 launch robot_bringup turtlesim_goal.launch.py 启动系统
理解 turtlesim_p_controller 和 robot_bringup 的边界
```

先记住一句话：

```text
功能包负责“我会做什么”，bringup 包负责“系统启动时把谁叫起来”。
```

## 一、为什么要有 robot_bringup

第 2 周第 1 小课里，launch 文件放在：

```text
src/turtlesim_p_controller/launch/turtlesim_goal.launch.py
```

这在入门阶段没有问题，因为当时只有一个控制器功能包。

但真实机器人系统会越来越大，例如：

```text
robot_description
yolo_detector
target_tracker
target_controller
navigation_task
```

如果每个功能包都放自己的启动入口，最后你会很难回答：

```text
我到底应该运行哪个 launch 文件来启动整套系统？
```

所以通常会单独创建一个 bringup 包：

```text
robot_bringup
```

它的职责是：

```text
统一启动多个 package 中的节点
统一加载系统启动需要的配置
给整套系统提供一个清晰入口
```

## 二、当前 workspace 结构

本课之后，`src/` 下有两个 package：

```text
src/
├── turtlesim_p_controller/
└── robot_bringup/
```

它们的分工是：

```text
turtlesim_p_controller
= 控制器功能包
= 提供 turtle_goal_controller 节点
= 保存控制器默认参数
= 测试控制数学和控制器资产

robot_bringup
= 启动编排包
= 不写控制算法
= 不新增控制节点
= 用 launch 文件启动 turtlesim 和 turtle_goal_controller
```

现在有两个启动入口：

```bash
ros2 launch turtlesim_p_controller turtlesim_goal.launch.py
ros2 launch robot_bringup turtlesim_goal.launch.py
```

学习重点是第二个：

```bash
ros2 launch robot_bringup turtlesim_goal.launch.py
```

它表示：

```text
从 robot_bringup 这个启动编排包里启动整套 turtlesim 控制系统
```

## 三、robot_bringup 目录结构

当前包结构：

```text
robot_bringup/
├── README.md
├── WEEK_02_02_ROBOT_BRINGUP_PACKAGE.md
├── package.xml
├── setup.py
├── setup.cfg
├── resource/
│   └── robot_bringup
├── launch/
│   └── turtlesim_goal.launch.py
├── test/
│   └── test_bringup_assets.py
└── robot_bringup/
    └── __init__.py
```

每个文件的职责：

- `package.xml`：声明这是一个 ROS 2 package，以及运行时依赖哪些包。
- `setup.py`：告诉 `colcon build` 要安装哪些 Python 模块和 launch 文件。
- `setup.cfg`：配置脚本安装目录，保持 `ament_python` 包结构完整。
- `resource/robot_bringup`：让 ROS 2 package index 能发现这个包。
- `launch/turtlesim_goal.launch.py`：统一启动 turtlesim 和控制器。
- `test/test_bringup_assets.py`：检查 bringup 包资产是否完整。
- `robot_bringup/__init__.py`：Python package 标记文件。

注意：

```text
robot_bringup 现在没有自己的节点。
```

这是正常的。bringup 包可以只包含 launch 文件。

## 四、launch 文件解释

源码：

```python
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    controller_share = get_package_share_directory("turtlesim_p_controller")
    controller_params = os.path.join(controller_share, "config", "goal_controller.yaml")

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

关键点 1：

```python
controller_share = get_package_share_directory("turtlesim_p_controller")
```

`robot_bringup` 自己不保存控制器参数，而是去找：

```text
turtlesim_p_controller 的安装 share 目录
```

关键点 2：

```python
controller_params = os.path.join(controller_share, "config", "goal_controller.yaml")
```

参数文件仍然来自：

```text
turtlesim_p_controller/config/goal_controller.yaml
```

这样做的理由是：

```text
控制器默认参数属于控制器功能包
bringup 负责引用它，而不是复制一份
```

关键点 3：

```python
Node(package="turtlesim", executable="turtlesim_node")
```

这个 Node 启动系统自带的 turtlesim。

关键点 4：

```python
Node(package="turtlesim_p_controller", executable="turtle_goal_controller")
```

这个 Node 启动你自己写的控制器。

所以 `robot_bringup` 的 launch 文件跨了两个包：

```text
turtlesim
turtlesim_p_controller
```

## 五、package.xml 解释

关键依赖：

```xml
<exec_depend>ament_index_python</exec_depend>
<exec_depend>launch</exec_depend>
<exec_depend>launch_ros</exec_depend>
<exec_depend>turtlesim</exec_depend>
<exec_depend>turtlesim_p_controller</exec_depend>
```

这些依赖的含义：

- `ament_index_python`：launch 文件用它查找其他 package 的 share 目录。
- `launch`：ROS 2 launch 基础库。
- `launch_ros`：提供 `Node(...)` 这种 ROS 节点启动动作。
- `turtlesim`：因为 bringup 要启动 `turtlesim_node`。
- `turtlesim_p_controller`：因为 bringup 要启动你的控制器节点，并读取它的参数文件。

`robot_bringup` 本身不发布 topic，也不订阅 topic。

它的依赖来自：

```text
它要启动谁
它要读取谁的配置
```

## 六、setup.py 解释

关键配置：

```python
data_files=[
    ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
    (os.path.join("share", package_name), ["package.xml"]),
    (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
],
```

这三行分别安装：

- ROS 2 package index 标记文件
- `package.xml`
- launch 文件

因为 `robot_bringup` 只负责启动编排，所以它目前不需要安装 config 文件。

构建后，launch 文件会出现在：

```text
install/robot_bringup/share/robot_bringup/launch/turtlesim_goal.launch.py
```

`ros2 launch robot_bringup turtlesim_goal.launch.py` 找的就是这个安装后的文件。

## 七、src/build/install/log 是什么

在 workspace 根目录：

```text
/home/sheepyjb/ros
```

你会看到：

```text
src/
build/
install/
log/
```

### 1. src/

源码目录。

你自己主要编辑这里：

```text
src/turtlesim_p_controller
src/robot_bringup
```

### 2. build/

构建过程的中间文件目录。

`colcon build` 会在这里临时处理 package。

一般不手动改。

### 3. install/

安装结果目录。

运行时 `ros2 run` 和 `ros2 launch` 主要从这里找包、节点、launch 文件和配置文件。

所以每次新终端要执行：

```bash
source /home/sheepyjb/ros/install/setup.bash
```

### 4. log/

构建日志目录。

当 `colcon build` 出错时，可以在这里找更详细的日志。

## 八、构建和运行

回到 workspace 根目录：

```bash
cd /home/sheepyjb/ros
```

加载系统 ROS 2：

```bash
source /opt/ros/jazzy/setup.bash
```

构建两个包：

```bash
colcon build --packages-select turtlesim_p_controller robot_bringup
```

加载当前 workspace：

```bash
source install/setup.bash
```

用 bringup 包启动系统：

```bash
ros2 launch robot_bringup turtlesim_goal.launch.py
```

另开终端检查：

```bash
source /opt/ros/jazzy/setup.bash
source /home/sheepyjb/ros/install/setup.bash
ros2 node list --no-daemon
```

应该看到：

```text
/turtlesim
/turtle_goal_controller
```

## 九、练习题

### 练习 1：对比两个 package

打开：

```text
src/turtlesim_p_controller
src/robot_bringup
```

回答：

- 哪个包有控制器 Python 节点？
- 哪个包只负责启动？
- 哪个包保存控制器参数 YAML？

### 练习 2：用 robot_bringup 启动系统

运行：

```bash
source /opt/ros/jazzy/setup.bash
cd /home/sheepyjb/ros
colcon build --packages-select turtlesim_p_controller robot_bringup
source install/setup.bash
ros2 launch robot_bringup turtlesim_goal.launch.py
```

观察 turtlesim 是否启动，乌龟是否向目标点运动。

### 练习 3：检查节点

另开终端：

```bash
source /opt/ros/jazzy/setup.bash
source /home/sheepyjb/ros/install/setup.bash
ros2 node list --no-daemon
```

写下你看到的节点。

### 练习 4：检查 launch 文件安装位置

运行：

```bash
find install/robot_bringup/share/robot_bringup -maxdepth 3 -type f | sort
```

确认里面有：

```text
launch/turtlesim_goal.launch.py
```

### 练习 5：解释跨包引用参数

打开：

```text
src/robot_bringup/launch/turtlesim_goal.launch.py
```

回答：

- `get_package_share_directory("turtlesim_p_controller")` 找的是哪个包？
- 为什么不是 `get_package_share_directory("robot_bringup")`？
- 参数 YAML 最终来自哪个 package？

### 练习 6：运行测试

运行：

```bash
python3 -m unittest src/robot_bringup/test/test_bringup_assets.py
```

再运行全部测试：

```bash
PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test
python3 -m unittest discover -s src/robot_bringup/test
```

## 十、参考答案要点

### 练习 1

- 有控制器节点的是 `turtlesim_p_controller`。
- 只负责启动的是 `robot_bringup`。
- 保存控制器参数 YAML 的是 `turtlesim_p_controller`。

### 练习 2

`ros2 launch robot_bringup turtlesim_goal.launch.py` 应该能启动两个节点：

```text
/turtlesim
/turtle_goal_controller
```

### 练习 3

应该看到：

```text
/turtlesim
/turtle_goal_controller
```

如果只看到 `/turtlesim`，说明控制器没启动或已经退出。

如果一个都看不到，先检查两个终端是否都 source 了环境。

### 练习 4

应该能看到：

```text
install/robot_bringup/share/robot_bringup/launch/turtlesim_goal.launch.py
```

这说明 `setup.py` 的 `data_files` 生效了。

### 练习 5

`get_package_share_directory("turtlesim_p_controller")` 找的是控制器功能包。

因为参数文件属于控制器包：

```text
src/turtlesim_p_controller/config/goal_controller.yaml
```

`robot_bringup` 只是启动编排包，负责引用这个参数文件。

### 练习 6

测试通过说明：

- `robot_bringup/package.xml` 存在。
- `robot_bringup/setup.py` 存在。
- launch 文件存在。
- `setup.py` 会安装 launch 文件。
- `package.xml` 声明了启动所需依赖。

## 十一、通过标准

完成本课后，你应该能做到：

- 解释 `turtlesim_p_controller` 和 `robot_bringup` 的区别。
- 解释为什么真实机器人项目常有 bringup 包。
- 说清楚 `src/`、`build/`、`install/`、`log/` 的作用。
- 用 `robot_bringup` 启动 turtlesim 控制系统。
- 解释 launch 文件如何跨 package 启动节点和读取参数。
- 知道 `ros2 launch` 读取的是安装后的 launch 文件，不是直接读取源码目录。

## 十二、本课总结

第 1 节解决的是：

```text
怎样写 launch 和 YAML 参数
```

第 2 节解决的是：

```text
这些 launch 文件应该放在哪个 package 里
```

当前项目的组织方式是：

```text
turtlesim_p_controller 负责控制器能力
robot_bringup 负责启动整套系统
```

这就是后续仿真机器人项目的基本组织方式。
