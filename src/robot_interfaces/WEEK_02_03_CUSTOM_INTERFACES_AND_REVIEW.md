# 第 2 周第 3 小课：自定义接口与综合练习

这份文档对应第 2 周第 3 小课，也是第 2 周最后一节：创建自定义接口包，并把自定义 service 接入 turtlesim 控制器。

本课目标：

```text
理解 ROS 2 自定义 msg/srv 的作用、接口包的结构，以及接口如何被其他 package 使用。
```

本课要学：

```text
robot_interfaces
msg
srv
rosidl_generate_interfaces
ros2 interface show
ros2 service call
接口包和功能包的依赖关系
```

本课练习：

```text
创建 robot_interfaces 接口包
定义 TargetDetection.msg
定义 SetGoal.srv
让 turtle_goal_controller 提供 /set_goal 服务
用 robot_bringup 启动系统后，通过自定义 service 修改目标点
```

先记住一句话：

```text
接口包只定义“数据长什么样”，不负责“谁来处理这些数据”。
```

## 一、为什么需要自定义接口

ROS 2 自带很多消息类型，比如：

```text
geometry_msgs/msg/Twist
turtlesim/msg/Pose
std_srvs/srv/Empty
```

但真实项目经常有自己的数据。

例如 YOLO 检测结果可能包含：

```text
类别名
置信度
检测框中心点
检测框宽高
是否正在跟踪
```

这些字段不是 `Twist` 或 `Pose` 能表达的，所以要定义自己的 msg。

再比如当前控制器原来通过参数改目标点：

```bash
ros2 param set /turtle_goal_controller goal_x 2.0
ros2 param set /turtle_goal_controller goal_y 8.0
```

这能用，但不够像“业务接口”。本课新增一个 service：

```text
robot_interfaces/srv/SetGoal
```

以后可以这样改目标点：

```bash
ros2 service call /set_goal robot_interfaces/srv/SetGoal "{x: 2.0, y: 8.0}"
```

这比直接改参数更像一个明确的功能：

```text
请求控制器设置新目标点
```

## 二、当前三个 package 的分工

第 2 周结束后，`src/` 下有三个 package：

```text
src/
├── robot_interfaces/
├── turtlesim_p_controller/
└── robot_bringup/
```

分工如下：

```text
robot_interfaces
= 接口包
= 定义 msg/srv
= 不启动节点
= 不写控制算法

turtlesim_p_controller
= 功能包
= 实现 turtle_goal_controller 节点
= 使用 robot_interfaces/srv/SetGoal

robot_bringup
= 启动编排包
= 用 launch 一次启动 turtlesim 和控制器
```

依赖方向是：

```text
turtlesim_p_controller -> robot_interfaces
robot_bringup -> turtlesim_p_controller
```

意思是：

```text
控制器功能包使用接口包
启动包启动控制器功能包
```

## 三、robot_interfaces 目录结构

当前包结构：

```text
robot_interfaces/
├── README.md
├── WEEK_02_03_CUSTOM_INTERFACES_AND_REVIEW.md
├── CMakeLists.txt
├── package.xml
├── msg/
│   └── TargetDetection.msg
├── srv/
│   └── SetGoal.srv
└── test/
    └── test_interface_assets.py
```

注意这个包没有：

```text
setup.py
Python 节点
launch 文件
```

因为它是 `ament_cmake` 接口包，不是 `ament_python` 节点包。

## 四、TargetDetection.msg

源码：

```text
string label
float32 confidence
float32 center_x
float32 center_y
float32 width
float32 height
bool is_tracking
```

字段含义：

- `label`：检测类别，比如 `person`、`cup`、`target`。
- `confidence`：置信度，比如 `0.92`。
- `center_x`：检测框中心 x，当前用归一化坐标表示。
- `center_y`：检测框中心 y，当前用归一化坐标表示。
- `width`：检测框宽度。
- `height`：检测框高度。
- `is_tracking`：是否正在跟踪这个目标。

这个 msg 以后可以给 YOLO 节点使用。

当前阶段先用命令行模拟发布：

```bash
ros2 topic pub --once /target_detection robot_interfaces/msg/TargetDetection \
  "{label: 'person', confidence: 0.92, center_x: 0.5, center_y: 0.4, width: 0.2, height: 0.3, is_tracking: true}"
```

另一个终端可以 echo：

```bash
ros2 topic echo /target_detection
```

## 五、SetGoal.srv

源码：

```text
float64 x
float64 y
---
bool success
string message
```

`---` 上面是请求：

```text
x
y
```

`---` 下面是响应：

```text
success
message
```

它表达的是：

```text
客户端请求设置目标点 x/y
服务端返回是否成功和提示消息
```

在当前项目里，服务端是：

```text
/turtle_goal_controller
```

服务名是：

```text
/set_goal
```

调用方式：

```bash
ros2 service call /set_goal robot_interfaces/srv/SetGoal "{x: 2.0, y: 8.0}"
```

## 六、CMakeLists.txt 解释

源码：

```cmake
cmake_minimum_required(VERSION 3.8)
project(robot_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/TargetDetection.msg"
  "srv/SetGoal.srv"
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
```

关键点：

```cmake
find_package(rosidl_default_generators REQUIRED)
```

这表示需要 ROS 2 的接口生成工具。

```cmake
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/TargetDetection.msg"
  "srv/SetGoal.srv"
)
```

这表示根据 `.msg` 和 `.srv` 文件生成不同语言可用的接口代码。

Python 节点里能写：

```python
from robot_interfaces.srv import SetGoal
```

就是因为构建时生成了 Python 侧接口代码。

## 七、package.xml 解释

关键内容：

```xml
<buildtool_depend>ament_cmake</buildtool_depend>
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

含义：

- `ament_cmake`：接口包使用 CMake 构建。
- `rosidl_default_generators`：构建时生成接口代码。
- `rosidl_default_runtime`：运行时让其他包使用生成的接口。
- `rosidl_interface_packages`：声明这是一个接口包。

## 八、控制器如何使用 SetGoal

`turtle_goal_controller.py` 里新增：

```python
from rclpy.parameter import Parameter
from robot_interfaces.srv import SetGoal
from turtlesim_p_controller.goal_service import validate_goal_coordinates
```

然后创建服务：

```python
self.create_service(SetGoal, "set_goal", self._on_set_goal)
```

当前节点没有设置额外 namespace，所以这个相对服务名会出现在 ROS 图里：

```text
/set_goal
```

注意：

```text
服务由 /turtle_goal_controller 节点创建
服务名当前是 /set_goal
```

服务回调会做三件事：

```text
读取请求中的 x/y
检查它们是不是有限数字
写入 goal_x 和 goal_y 参数
```

因为控制器每次收到 `/turtle1/pose` 都会重新读取参数，所以服务更新参数后，控制器会自动朝新目标点运动。

## 九、构建和运行

回到 workspace 根目录：

```bash
cd /home/sheepyjb/ros
```

构建三个包：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select robot_interfaces turtlesim_p_controller robot_bringup
source install/setup.bash
```

查看接口：

```bash
ros2 interface show robot_interfaces/msg/TargetDetection
ros2 interface show robot_interfaces/srv/SetGoal
```

启动系统：

```bash
ros2 launch robot_bringup turtlesim_goal.launch.py
```

另开终端：

```bash
source /opt/ros/jazzy/setup.bash
source /home/sheepyjb/ros/install/setup.bash
ros2 service list | grep set_goal
```

应该看到：

```text
/set_goal
```

调用自定义服务：

```bash
ros2 service call /set_goal robot_interfaces/srv/SetGoal "{x: 2.0, y: 8.0}"
```

成功时可能先短暂显示：

```text
waiting for service to become available...
```

只要后面继续出现请求和响应，就说明已经调用成功：

```text
requester: making request: robot_interfaces.srv.SetGoal_Request(x=2.0, y=8.0)

response:
robot_interfaces.srv.SetGoal_Response(success=True, message='目标点已更新为 (2.00, 8.00)。')
```

观察乌龟是否朝新目标点运动。

如果调用服务时一直显示：

```text
waiting for service to become available...
```

按这个顺序排查：

```bash
ros2 service list | grep set_goal
ros2 node list --no-daemon
```

如果 `ros2 interface show robot_interfaces/srv/SetGoal` 能显示接口，但 `ros2 service list` 看不到 `/set_goal`，说明只是接口包构建好了，控制器节点还没有启动新服务。通常需要先停掉旧 launch：

```text
Ctrl+C
```

然后重新构建、source、启动：

```bash
colcon build --packages-select robot_interfaces turtlesim_p_controller robot_bringup
source install/setup.bash
ros2 launch robot_bringup turtlesim_goal.launch.py
```

另外，命令是 `ros2`，不是 `os2`。

## 十、练习题

### 练习 1：查看自定义接口

运行：

```bash
ros2 interface show robot_interfaces/msg/TargetDetection
ros2 interface show robot_interfaces/srv/SetGoal
```

回答：

- `TargetDetection.msg` 有哪些字段？
- `SetGoal.srv` 的请求字段是什么？
- `SetGoal.srv` 的响应字段是什么？

### 练习 2：模拟发布检测结果

终端 1：

```bash
ros2 topic echo /target_detection
```

终端 2：

```bash
ros2 topic pub --once /target_detection robot_interfaces/msg/TargetDetection \
  "{label: 'person', confidence: 0.92, center_x: 0.5, center_y: 0.4, width: 0.2, height: 0.3, is_tracking: true}"
```

观察终端 1 是否收到消息。

### 练习 3：启动系统并查看服务

运行：

```bash
ros2 launch robot_bringup turtlesim_goal.launch.py
```

另开终端：

```bash
ros2 service list | grep set_goal
```

### 练习 4：用自定义服务修改目标点

运行：

```bash
ros2 service call /set_goal robot_interfaces/srv/SetGoal "{x: 2.0, y: 8.0}"
```

观察：

- 服务返回是否 `success: true`
- 乌龟是否朝新目标点运动
- 控制器终端是否打印目标点更新日志

### 练习 5：对比 param 和 service

分别运行：

```bash
ros2 param set /turtle_goal_controller goal_x 8.0
ros2 param set /turtle_goal_controller goal_y 2.0
```

和：

```bash
ros2 service call /set_goal robot_interfaces/srv/SetGoal "{x: 8.0, y: 2.0}"
```

回答：

- 哪个更像直接改配置？
- 哪个更像调用控制器功能？

### 练习 6：运行测试

运行：

```bash
python3 -m unittest discover -s src/robot_interfaces/test
PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test
python3 -m unittest discover -s src/robot_bringup/test
```

## 十一、参考答案要点

### 练习 1

`TargetDetection.msg` 有类别、置信度、检测框位置尺寸和跟踪状态字段。

`SetGoal.srv` 请求字段是：

```text
x
y
```

响应字段是：

```text
success
message
```

### 练习 2

`ros2 topic pub` 发布的是一条自定义 msg，`ros2 topic echo` 可以看到同样字段。

这说明接口包生成的消息类型可以被 ROS 2 topic 使用。

### 练习 3

应该看到：

```text
/set_goal
```

这个服务由 `turtle_goal_controller` 节点创建。

### 练习 4

服务应该返回类似：

```text
success: true
message: 目标点已更新为 (2.00, 8.00)。
```

然后控制器更新 `goal_x` 和 `goal_y` 参数，乌龟朝新目标点运动。

### 练习 5

`ros2 param set` 更像直接改配置。

`ros2 service call` 更像调用控制器提供的功能接口。

以后复杂系统里，任务节点通常更适合调用 service/action，而不是直接改别人的内部参数。

### 练习 6

测试通过说明：

- `robot_interfaces` 接口文件存在。
- `package.xml` 和 `CMakeLists.txt` 包含接口生成配置。
- 控制器的目标点校验逻辑正确。
- bringup 包资产仍然完整。

## 十二、第 2 周总结

第 2 周三节课分别解决：

```text
第 1 节：怎么用 launch 和 YAML 启动、配置节点
第 2 节：为什么要用 robot_bringup 统一启动系统
第 3 节：怎么定义自己的 msg/srv，并让功能包使用它
```

到这里，你已经见过三类 package：

```text
接口包：robot_interfaces
功能包：turtlesim_p_controller
启动包：robot_bringup
```

这是 ROS 2 项目最常见的基础组织方式。

## 十三、通过标准

完成本课后，你应该能做到：

- 解释 msg 和 srv 的区别。
- 解释为什么接口包通常用 `ament_cmake`。
- 用 `ros2 interface show` 查看自定义接口。
- 用 `ros2 topic pub` 发布自定义 msg。
- 用 `ros2 service call` 调用自定义 srv。
- 解释 `robot_interfaces`、`turtlesim_p_controller`、`robot_bringup` 三个包的分工。
- 解释为什么服务调用比直接改参数更像“功能接口”。
