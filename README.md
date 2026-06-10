# ROS 2 学习仓库

这个仓库用于记录 ROS 2 学习笔记，并保存每周的小练习代码。

## 当前环境建议

- Ubuntu 24.04 LTS
- ROS 2 Jazzy Jalisco

## 目录结构

```text
.
├── ros2_learning_notes.md
└── src/
    └── turtlesim_p_controller/
```

## 第一个练习

`src/turtlesim_p_controller` 是第 1 周练习：用 P 控制让 turtlesim 乌龟移动到固定目标点。

本地纯 Python 测试：

```bash
PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test
```

安装 ROS 2 Jazzy 后运行：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select turtlesim_p_controller
source install/setup.bash
```

终端 1：

```bash
ros2 run turtlesim turtlesim_node
```

终端 2：

```bash
ros2 run turtlesim_p_controller turtle_goal_controller
```

第 2 周开始，也可以用 launch 文件一次启动两个节点：

```bash
ros2 launch turtlesim_p_controller turtlesim_goal.launch.py
```

创建 `robot_bringup` 包后，推荐用启动编排包作为系统入口：

```bash
colcon build --packages-select turtlesim_p_controller robot_bringup
source install/setup.bash
ros2 launch robot_bringup turtlesim_goal.launch.py
```

参数默认值在：

```text
src/turtlesim_p_controller/config/goal_controller.yaml
```

## Git 使用

查看状态：

```bash
git status --short --branch
```

查看改动：

```bash
git diff
```

提交：

```bash
git add README.md ros2_learning_notes.md src/turtlesim_p_controller
git commit -m "Add ROS 2 learning notes and turtlesim P controller"
```
