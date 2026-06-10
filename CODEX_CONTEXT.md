# CODEX_CONTEXT

## Latest Snapshot

Date: 2026-06-10

Current goal:

- 第 1 周 ROS 2 基础通信学习已完成。
- 第 2 周工作空间、包和接口学习已完成。
- 下一步进入第 3 周第 1 小课：tf2 与 ROS 2 坐标系入门。

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
- 创建 ROS 2 Python 包 `src/robot_bringup`，作为启动编排包。
- 创建 `src/robot_bringup/launch/turtlesim_goal.launch.py`，从 bringup 包统一启动 `turtlesim_node` 和 `turtle_goal_controller`。
- 创建第 2 周第 2 小课讲义 `src/robot_bringup/WEEK_02_02_ROBOT_BRINGUP_PACKAGE.md`。
- 新增 `src/robot_bringup/test/test_bringup_assets.py`，测试 bringup 包结构、launch 安装声明和运行依赖。
- 更新 `README.md` 和 `ros2_learning_notes.md`，加入 `robot_bringup` 推荐启动入口。
- 创建 ROS 2 接口包 `src/robot_interfaces`，定义 `TargetDetection.msg` 和 `SetGoal.srv`。
- 创建第 2 周第 3 小课讲义 `src/robot_interfaces/WEEK_02_03_CUSTOM_INTERFACES_AND_REVIEW.md`。
- 新增 `src/robot_interfaces/test/test_interface_assets.py`，测试接口包结构、msg/srv 字段和依赖声明。
- 新增 `goal_service.py`，提供 `SetGoal` 服务复用的目标点校验逻辑。
- 更新 `turtle_goal_controller.py`，新增 `/set_goal` 自定义服务，可运行时设置目标点。
- 更新 `turtlesim_p_controller/package.xml`，声明对 `robot_interfaces` 的依赖。
- 用户已实操跑通 `/set_goal` 自定义服务，服务返回 `success=True`。
- 用户确认第 2 周第 3 小课已理解；第 2 周三节课均已完成。

Important decisions:

- 学习环境建议使用 Ubuntu 24.04 + ROS 2 Jazzy。
- 第一个练习只做 turtlesim P 控制，不引入 Gazebo/Nav2，降低第一周复杂度。
- 控制数学与 ROS 2 节点分离，原因是数学逻辑可以在没有 ROS 2 的环境中验证。
- 文档命名规则：整周课件使用 `WEEK_01_...`；第二周起的小课使用 `WEEK_02_01_...`、`WEEK_02_02_...`。
- 后续每一课都要配套练习题、观察问题、知识问答、参考答案和验收标准。
- 第 2 周第 1 小课先在原 `turtlesim_p_controller` 包内学习 launch/config，暂不新建 `robot_bringup`；后续小课再迁移到 bringup 包，降低概念密度。
- launch/config 是运行时资产，必须通过 `setup.py` 的 `data_files` 安装到 `install/<package>/share/<package>/`，否则 `ros2 launch` 找不到。
- 第 2 周调整为 3 节课：第 1 节 launch 与参数 YAML；第 2 节 `robot_bringup` 与工作空间组织；第 3 节自定义接口与综合练习。
- `robot_bringup` 当前不放控制算法和参数 YAML，只负责启动编排；控制器默认参数继续归属 `turtlesim_p_controller/config/goal_controller.yaml`。
- `robot_interfaces` 是纯接口包，使用 `ament_cmake` 和 `rosidl_generate_interfaces`；不放节点、不放 launch。
- 第 3 节让 `SetGoal.srv` 真正接入控制器；`TargetDetection.msg` 暂时用 CLI 模拟发布，为后续 YOLO 接入做概念准备。

Verification:

- 已运行纯 Python 单元测试：`PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test`。
- 已运行 Python 语法检查：`python3 -m compileall src/turtlesim_p_controller/turtlesim_p_controller`。
- 当前环境已安装 ROS 2 Jazzy。
- 已运行 `colcon build --packages-select turtlesim_p_controller`，构建通过。
- 已运行 `ros2 pkg executables turtlesim_p_controller`，确认入口为 `turtle_goal_controller`。
- 已运行 `ros2 launch turtlesim_p_controller turtlesim_goal.launch.py --show-args`，在 `ROS_LOG_DIR=/tmp/ros2_launch_logs` 下确认 launch 文件可被加载。
- 已运行 `colcon build --packages-select turtlesim_p_controller robot_bringup`，两个包构建通过。
- 已运行 `ros2 launch robot_bringup turtlesim_goal.launch.py --show-args`，在 `ROS_LOG_DIR=/tmp/ros2_launch_logs` 下确认 bringup launch 文件可被加载。
- 已运行 `colcon build --packages-select robot_interfaces turtlesim_p_controller robot_bringup`，三个包构建通过。
- 已运行 `ros2 interface show robot_interfaces/msg/TargetDetection` 和 `ros2 interface show robot_interfaces/srv/SetGoal`，确认自定义接口可发现。
- 已实际运行 turtlesim 图形窗口和控制器节点。
- 已使用 `/reset` 服务验证 service 调用。
- 已使用 rqt_graph 观察 `/turtlesim` 和 `/turtle_goal_controller` 的 topic 连接关系。

Remaining tasks:

- 开始第 3 周第 1 小课，建议命名为 `WEEK_03_01_TF2_FRAMES.md`。
- 学习 `map`、`odom`、`base_link` 等 frame 概念。
- 后续创建 `robot_description` 包，逐步进入 URDF / Xacro 和 RViz。

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
- `src/robot_bringup/WEEK_02_02_ROBOT_BRINGUP_PACKAGE.md`
- `src/robot_bringup/launch/turtlesim_goal.launch.py`
- `src/robot_bringup/package.xml`
- `src/robot_bringup/setup.py`
- `src/robot_bringup/test/test_bringup_assets.py`
- `src/robot_interfaces/WEEK_02_03_CUSTOM_INTERFACES_AND_REVIEW.md`
- `src/robot_interfaces/msg/TargetDetection.msg`
- `src/robot_interfaces/srv/SetGoal.srv`
- `src/robot_interfaces/CMakeLists.txt`
- `src/robot_interfaces/package.xml`
- `src/turtlesim_p_controller/turtlesim_p_controller/goal_service.py`

## Session Notes

### 2026-06-10

- Progress/result checkpoint:
  - 用户确认第 2 周第 3 小课已搞懂。
  - 第 2 周学习完成，已覆盖 launch/YAML、`robot_bringup`、`robot_interfaces`、自定义 msg/srv、三类 package 分工。
- Next:
  - 进入第 3 周：tf2、URDF 与 RViz。

### 2026-06-10

- Progress/result checkpoint:
  - 第 2 周第 3 小课材料已创建：`robot_interfaces` 接口包、自定义 msg/srv、控制器自定义服务、讲义和资产测试。
  - `TargetDetection.msg` 表示简化检测结果，当前用于 CLI 模拟发布，后续可服务于 YOLO 接入。
  - `SetGoal.srv` 已接入 `turtle_goal_controller`，当前服务名为 `/set_goal`，用于运行时更新目标点。
  - 用户实操确认：`ros2 service call /set_goal robot_interfaces/srv/SetGoal "{x: 2.0, y: 8.0}"` 返回 `success=True`。
  - 控制器新增 `goal_service.py`，将目标点坐标校验拆成纯 Python 函数并测试。
- Verification:
  - `python3 -m unittest discover -s src/robot_interfaces/test` 通过。
  - `PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test` 通过。
  - `python3 -m unittest discover -s src/robot_bringup/test` 通过。
  - `python3 -m compileall src/turtlesim_p_controller/turtlesim_p_controller src/turtlesim_p_controller/launch src/turtlesim_p_controller/test src/robot_bringup src/robot_interfaces` 通过。
  - `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_interfaces turtlesim_p_controller robot_bringup` 通过。
  - `ros2 interface show robot_interfaces/msg/TargetDetection` 和 `ros2 interface show robot_interfaces/srv/SetGoal` 可显示接口定义。
  - 设置 `ROS_LOG_DIR=/tmp/ros2_launch_logs` 后，`ros2 launch robot_bringup turtlesim_goal.launch.py --show-args` 通过。
- Next:
  - 带用户实操第 3 节；确认服务调用能让乌龟朝新目标点运动后再提交。

### 2026-06-10

- Progress/result checkpoint:
  - 第 2 周第 2 小课材料已创建：`robot_bringup` 包、bringup launch、讲义和资产测试。
  - `robot_bringup` 是启动编排包，不新增控制节点，不复制控制器参数；它通过 `get_package_share_directory("turtlesim_p_controller")` 引用控制器包的 YAML。
  - 新的推荐启动入口是 `ros2 launch robot_bringup turtlesim_goal.launch.py`。
  - 第一次尝试 `python3 -m unittest discover -s src` 没发现测试，已将讲义中的全部测试命令改为分别发现两个 test 目录。
- Verification:
  - `PYTHONPATH=src/turtlesim_p_controller python3 -m unittest discover -s src/turtlesim_p_controller/test` 通过。
  - `python3 -m unittest discover -s src/robot_bringup/test` 通过。
  - `python3 -m compileall src/turtlesim_p_controller/turtlesim_p_controller src/turtlesim_p_controller/launch src/turtlesim_p_controller/test src/robot_bringup` 通过。
  - `source /opt/ros/jazzy/setup.bash && colcon build --packages-select turtlesim_p_controller robot_bringup` 通过。
  - 设置 `ROS_LOG_DIR=/tmp/ros2_launch_logs` 后，`ros2 launch robot_bringup turtlesim_goal.launch.py --show-args` 通过。
- Next:
  - 带用户运行并理解 `robot_bringup`，尤其是 `src/build/install/log` 与功能包/启动包边界。

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
