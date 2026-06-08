# CODEX_CONTEXT

## Latest Snapshot

Date: 2026-06-08

Current goal:

- 建立 `/home/sheepyjb/ros` 为 git 管理的 ROS 2 学习仓库。
- 创建 ROS 2 学习计划笔记。
- 创建第 1 周 turtlesim + P 控制练习。

Completed work:

- 初始化 git 仓库，默认分支为 `main`。
- 创建根目录说明 `README.md`。
- 创建学习笔记 `ros2_learning_notes.md`。
- 创建 ROS 2 Python 包 `src/turtlesim_p_controller`。
- 将 P 控制数学逻辑拆到 `controller_math.py`，便于无 ROS 环境下单元测试。
- 创建 `turtle_goal_controller.py` 作为 ROS 2 节点入口。
- 创建单元测试 `test_controller_math.py`。

Important decisions:

- 学习环境建议使用 Ubuntu 24.04 + ROS 2 Jazzy。
- 第一个练习只做 turtlesim P 控制，不引入 Gazebo/Nav2，降低第一周复杂度。
- 控制数学与 ROS 2 节点分离，原因是数学逻辑可以在没有 ROS 2 的环境中验证。

Verification:

- 已运行纯 Python 单元测试：`PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test`。
- 已运行 Python 语法检查：`python3 -m compileall src/turtlesim_p_controller/turtlesim_p_controller`。
- 当前环境已安装 ROS 2 Jazzy。
- 已运行 `colcon build --packages-select turtlesim_p_controller`，构建通过。
- 已运行 `ros2 pkg executables turtlesim_p_controller`，确认入口为 `turtle_goal_controller`。

Remaining tasks:

- 启动 `turtlesim_node` 和 `turtle_goal_controller`，观察乌龟是否移动到目标点。
- 根据实际运动效果调参：`linear_gain`、`angular_gain`、`max_linear_speed`、`max_angular_speed`。

Key files:

- `README.md`
- `ros2_learning_notes.md`
- `src/turtlesim_p_controller/CODE_WALKTHROUGH.md`
- `src/turtlesim_p_controller/turtlesim_p_controller/controller_math.py`
- `src/turtlesim_p_controller/turtlesim_p_controller/turtle_goal_controller.py`
- `src/turtlesim_p_controller/test/test_controller_math.py`

## Session Notes

### 2026-06-08

- 用户希望学习 ROS 2，并有 YOLO 深度学习基础和控制理论基础。
- 已制定 8 到 10 周路线，重点从 ROS 2 基础、turtlesim、tf2、URDF、Gazebo、YOLO 接入、控制、Nav2 到综合项目。
- 用户确认使用中文交流。
- 用户要求做 git 管理，仓库已初始化。
- 用户已在 Ubuntu 24.04 WSL2 中安装 ROS 2 Jazzy。
- 已构建第 1 周 `turtlesim_p_controller` 包并确认 ROS 2 可发现可执行入口。
- 已新增 `src/turtlesim_p_controller/CODE_WALKTHROUGH.md`，按 0 基础解释该 package 的目录、文件、配置和核心代码。
