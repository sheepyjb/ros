# CODEX_CONTEXT

## Latest Snapshot

Date: 2026-06-10

Current goal:

- 第 1 周 ROS 2 基础通信学习已完成。
- 第 2 周按 3 节课推进。
- 第 2 周第 1 小课 launch 文件与参数 YAML 已完成并已通过实操理解。
- 下一步进入第 2 周第 2 小课：`robot_bringup` 包与工作空间组织。

Completed work:

- 初始化 git 仓库，默认分支为 `main`。
- 创建根目录说明 `README.md`。
- 创建学习笔记 `ros2_learning_notes.md`。
- 创建 ROS 2 Python 包 `src/turtlesim_p_controller`。
- 将 P 控制数学逻辑拆到 `controller_math.py`，便于无 ROS 环境下单元测试。
- 创建 `turtle_goal_controller.py` 作为 ROS 2 节点入口。
- 创建单元测试 `test_controller_math.py`。
- 安装并验证 ROS 2 Jazzy 环境。
- 成功运行 `turtlesim_node` 和 `turtle_goal_controller`，完成 `/turtle1/pose` -> 控制器 -> `/turtle1/cmd_vel` 闭环。
- 通过调节 `linear_gain`、`angular_gain`、速度限幅和目标点，观察并理解了轨迹变化、绕圈原因、到达阈值停止和参数类型错误。
- 第一周课件已统一命名为 `src/turtlesim_p_controller/WEEK_01_ROS2_BASIC_COMMUNICATION.md`。
- 第一周课件已补充练习题、知识问答、参考答案、通过标准和 rqt_graph 系统结构图。
- 第一周核心代码已补充教学注释。
- 创建 `src/turtlesim_p_controller/launch/turtlesim_goal.launch.py`，可一次启动 `turtlesim_node` 和 `turtle_goal_controller`。
- 创建 `src/turtlesim_p_controller/config/goal_controller.yaml`，集中管理控制器默认参数。
- 更新 `setup.py`，安装 launch/config 文件到 package share 目录。
- 更新 `package.xml`，补充 `ament_index_python`、`launch`、`launch_ros` 运行依赖。
- 创建第 2 周第 1 小课讲义 `src/turtlesim_p_controller/WEEK_02_01_LAUNCH_AND_PARAMS.md`。
- 更新 `README.md` 和 `ros2_learning_notes.md`，加入 `ros2 launch` 运行方式。
- 新增 `test_launch_assets.py`，测试 launch/config 文件存在并且 `setup.py` 包含安装声明。
- 用户已通过实操理解 `source`、`colcon build`、`ros2 launch`、YAML 参数默认值、`ros2 param set` 临时参数、`/cmd_vel` 与 `/pose` 的区别，以及 `ros2 node list --no-daemon` 的排查价值。

Important decisions:

- 学习环境建议使用 Ubuntu 24.04 + ROS 2 Jazzy。
- 第一个练习只做 turtlesim P 控制，不引入 Gazebo/Nav2，降低第一周复杂度。
- 控制数学与 ROS 2 节点分离，原因是数学逻辑可以在没有 ROS 2 的环境中验证。
- 文档命名规则：整周课件使用 `WEEK_01_...`；第二周起的小课使用 `WEEK_02_01_...`、`WEEK_02_02_...`。
- 后续每一课都要配套练习题、观察问题、知识问答、参考答案和验收标准。
- 第 2 周第 1 小课先在原 `turtlesim_p_controller` 包内学习 launch/config，暂不新建 `robot_bringup`；后续小课再迁移到 bringup 包，降低概念密度。
- launch/config 是运行时资产，必须通过 `setup.py` 的 `data_files` 安装到 `install/<package>/share/<package>/`，否则 `ros2 launch` 找不到。
- 第 2 周调整为 3 节课：第 1 节 launch 与参数 YAML；第 2 节 `robot_bringup` 与工作空间组织；第 3 节自定义接口与综合练习。

Verification:

- 已运行纯 Python 单元测试：`PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test`。
- 已运行 Python 语法检查：`python3 -m compileall src/turtlesim_p_controller/turtlesim_p_controller`。
- 当前环境已安装 ROS 2 Jazzy。
- 已运行 `colcon build --packages-select turtlesim_p_controller`，构建通过。
- 已运行 `ros2 pkg executables turtlesim_p_controller`，确认入口为 `turtle_goal_controller`。
- 已运行 `ros2 launch turtlesim_p_controller turtlesim_goal.launch.py --show-args`，在 `ROS_LOG_DIR=/tmp/ros2_launch_logs` 下确认 launch 文件可被加载。
- 已实际运行 turtlesim 图形窗口和控制器节点。
- 已使用 `/reset` 服务验证 service 调用。
- 已使用 rqt_graph 观察 `/turtlesim` 和 `/turtle_goal_controller` 的 topic 连接关系。

Remaining tasks:

- 开始第 2 周第 2 小课，建议命名为 `WEEK_02_02_ROBOT_BRINGUP_PACKAGE.md`。
- 创建 `robot_bringup` 包，学习 bringup 包的职责。
- 将 turtlesim 启动文件作为练习迁移或复制到 `robot_bringup`，理解功能包与启动编排包的区别。
- 第 2 周第 3 小课再创建自定义接口包，并做综合练习。

Key files:

- `README.md`
- `ros2_learning_notes.md`
- `src/turtlesim_p_controller/WEEK_01_ROS2_BASIC_COMMUNICATION.md`
- `src/turtlesim_p_controller/WEEK_02_01_LAUNCH_AND_PARAMS.md`
- `src/turtlesim_p_controller/assets/rqt_graph_turtlesim_controller.svg`
- `src/turtlesim_p_controller/launch/turtlesim_goal.launch.py`
- `src/turtlesim_p_controller/config/goal_controller.yaml`
- `src/turtlesim_p_controller/turtlesim_p_controller/controller_math.py`
- `src/turtlesim_p_controller/turtlesim_p_controller/turtle_goal_controller.py`
- `src/turtlesim_p_controller/test/test_controller_math.py`
- `src/turtlesim_p_controller/test/test_launch_assets.py`

## Session Notes

### 2026-06-10

- Progress/result checkpoint:
  - 用户确认第 2 周第 1 小课已搞懂，可以进入第 2 小课。
  - 第 2 周课程规划调整为 3 节：launch/参数、`robot_bringup`/工作空间组织、自定义接口/综合练习。
  - 第 1 节学习中重点澄清：
    - `source /opt/ros/jazzy/setup.bash` 让终端认识系统 ROS 2。
    - `colcon build --packages-select turtlesim_p_controller` 构建当前包并生成 `install/`。
    - `source install/setup.bash` 让终端认识当前 workspace 构建出的包。
    - `ros2 param set` 只改运行中节点的内存参数，不写回 YAML。
    - `ros2 topic echo /turtle1/cmd_vel --once` 只读取执行后收到的第一条速度命令，不代表历史速度。
    - `/cmd_vel` 是控制命令，`/pose` 中的 velocity 是 turtlesim 当前状态。
    - `ros2 node list --no-daemon` 更适合排查 daemon 缓存或节点发现延迟。
- Next:
  - 开始 `WEEK_02_02_ROBOT_BRINGUP_PACKAGE.md`，创建并讲解 `robot_bringup` 包。

### 2026-06-09

- Progress/result checkpoint:
  - 第 2 周第 1 小课 launch 文件与参数 YAML 已完成。
  - 新增 `launch/turtlesim_goal.launch.py`，可用 `ros2 launch turtlesim_p_controller turtlesim_goal.launch.py` 一次启动 turtlesim 和控制器。
  - 新增 `config/goal_controller.yaml`，保存 `goal_x`、`goal_y`、`linear_gain`、`angular_gain`、速度限幅和到达阈值。
  - 更新 `setup.py` 的 `data_files`，安装 launch/config 文件。
  - 更新 `package.xml`，补充 launch 相关运行依赖。
  - 新增 `test_launch_assets.py`，用测试约束 launch/config 资产和安装声明。
  - 创建 `WEEK_02_01_LAUNCH_AND_PARAMS.md`，包含概念解释、运行命令、练习题、参考答案和通过标准。
  - 更新 `README.md` 和 `ros2_learning_notes.md`。
- Verification:
  - `PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test` 通过。
  - `python3 -m compileall src/turtlesim_p_controller/turtlesim_p_controller src/turtlesim_p_controller/launch src/turtlesim_p_controller/test` 通过。
  - `source /opt/ros/jazzy/setup.bash && colcon build --packages-select turtlesim_p_controller` 通过。
  - `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ros2 pkg executables turtlesim_p_controller` 确认入口。
  - 设置 `ROS_LOG_DIR=/tmp/ros2_launch_logs` 后，`ros2 launch turtlesim_p_controller turtlesim_goal.launch.py --show-args` 通过。
- Next:
  - 第 2 周第 2 小课建议创建 `robot_bringup` 包，讲清楚功能包和 bringup 包的边界。

### 2026-06-09

- Progress/result checkpoint:
  - 第一周 ROS 2 基础通信已完成。
  - 已掌握并实践 `ros2 node`、`ros2 topic`、`ros2 service`、`ros2 action`、`ros2 param`、`rqt_graph` 和 `turtlesim`。
  - 已能解释 `/turtle1/pose` 和 `/turtle1/cmd_vel` 的消息方向。
  - 已能调节 P 控制参数并解释 `linear_gain`、`angular_gain` 对轨迹的影响。
  - 已能解释角速度为什么要根据角度误差闭环控制。
  - 结果：可以进入第 2 周学习。
- 用户确认第 1 周 turtlesim P 控制内容已掌握，要求第一周文档与学习计划保持一致。
- 已将第一周逐文件讲解文档统一命名为 `WEEK_01_ROS2_BASIC_COMMUNICATION.md`。
- 第一周文档已补充本周目标、要学命令、练习题、知识问答、参考答案要点和通过标准。
- 约定后续第二周小课使用 `WEEK_02_01_...`、`WEEK_02_02_...` 命名。
- 已按用户要求将第一周核心代码的逐行解释补进源码注释，涉及 `controller_math.py`、`turtle_goal_controller.py` 和 `test_controller_math.py`。
- 已在第一周文档的 rqt_graph 练习中加入系统结构图 `assets/rqt_graph_turtlesim_controller.svg`，并为练习 1 到练习 10 补充对应参考答案。

### 2026-06-08

- 用户希望学习 ROS 2，并有 YOLO 深度学习基础和控制理论基础。
- 已制定 8 到 10 周路线，重点从 ROS 2 基础、turtlesim、tf2、URDF、Gazebo、YOLO 接入、控制、Nav2 到综合项目。
- 用户确认使用中文交流。
- 用户要求做 git 管理，仓库已初始化。
- 用户已在 Ubuntu 24.04 WSL2 中安装 ROS 2 Jazzy。
- 已构建第 1 周 `turtlesim_p_controller` 包并确认 ROS 2 可发现可执行入口。
- 已将第一周文档命名为 `src/turtlesim_p_controller/WEEK_01_ROS2_BASIC_COMMUNICATION.md`，按 0 基础解释该 package 的目录、文件、配置和核心代码，并补充第一周练习题、知识问答和通过标准。
- 后续第二周小课采用 `WEEK_02_01_...`、`WEEK_02_02_...` 这种命名，表示第 2 周第 1/2 小课。
