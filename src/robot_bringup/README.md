# robot_bringup

`robot_bringup` 是第 2 周第 2 节的启动编排包。

它不实现控制算法，也不定义新的节点。它负责用 launch 文件把已有功能包组合起来启动。

当前启动命令：

```bash
ros2 launch robot_bringup turtlesim_goal.launch.py
```

第 3 周第 3 小课开始，模型显示也可以从 bringup 入口启动：

```bash
ros2 launch robot_bringup display_robot.launch.py
```

本节讲义：

```text
WEEK_02_02_ROBOT_BRINGUP_PACKAGE.md
```
