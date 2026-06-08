# turtlesim_p_controller

第 1 周练习：用 P 控制让 turtlesim 乌龟移动到固定目标点。

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
