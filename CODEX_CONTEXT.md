# CODEX_CONTEXT

## Latest Snapshot

Date: 2026-06-16

Current goal:

- 第 1 周 ROS 2 基础通信学习已完成。
- 第 2 周工作空间、包和接口学习已完成。
- 第 3 周第 1 小课：tf2 与 ROS 2 坐标系入门已完成。
- 第 3 周第 2 小课：`robot_description`、URDF、轮子、摄像头和雷达 frame 已完成并实操验证。
- 第 3 周第 3 小课：Xacro、可复用 RViz/bringup 启动和更完整模型组织已完成代码与讲义准备。
- 第 4 周第 1 小课：Gazebo Harmonic 与 `ros_gz` 最小链路已完成代码、讲义和实机验证。
- 第 4 周第 2 小课：差速小车 Gazebo 运动、`/cmd_vel` 和 `/odom` bridge 已完成代码、讲义和实机验证。
- 第 4 周第 3 小课：键盘控制、雷达、相机、TF/RViz 同步显示已完成代码、讲义和验证。
- 第 4 周第 2/3 小课 Gazebo 小车已从单后 caster 改为前后两个 caster，修复原地转向时绕轮轴翘起的问题。
- 下一步进入第 5 周：YOLO 接入 ROS 2 图像链路。

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
- 创建 ROS 2 Python 包 `src/tf2_frame_demo`，用于第 3 周第 1 小课 tf2 坐标系入门。
- 新增 `frame_math.py`，提供 yaw/四元数转换、圆周运动位姿和角度归一化的纯 Python 数学逻辑。
- 新增 `dynamic_frame_broadcaster.py`，发布 `odom -> base_link` 动态 TF。
- 新增 `frame_listener.py`，查询 `map -> camera_link` 并打印位置和 yaw。
- 修复 `dynamic_frame_broadcaster.py` 和 `frame_listener.py` 的 Ctrl-C 退出路径，避免重复 `rclpy.shutdown()` 导致 traceback。
- 新增 `launch/tf2_demo.launch.py`，一次启动 `map -> odom`、`odom -> base_link`、`base_link -> camera_link` 这棵 TF 树。
- 创建第 3 周第 1 小课讲义 `src/tf2_frame_demo/WEEK_03_01_TF2_FRAMES.md`。
- 第 3 周第 1 小课已正式加入 RViz2 可视化观察步骤：`Fixed Frame = map`，添加 `TF` display，观察坐标轴、frame 名称和黄色父子关系线。
- 第 3 周第 1 小课核心代码已补充教学注释，覆盖 `frame_math.py`、`dynamic_frame_broadcaster.py`、`frame_listener.py` 和 `tf2_demo.launch.py`。
- 新增 `test_frame_math.py`、`test_tf2_frame_demo_assets.py` 和 `test_node_shutdown.py`，测试数学逻辑、package/launch 资产和 Ctrl-C 退出路径。
- 更新 `README.md` 和 `ros2_learning_notes.md`，加入第 3 周第 1 小课入口。
- 创建 ROS 2 Python 资源包 `src/robot_description`，用于第 3 周第 2 小课 URDF 和机器人模型显示。
- 新增 `urdf/diffbot.urdf`，描述简化差速小车的 `base_link`、左右轮、`camera_link`、`camera_optical_frame` 和 `laser_link`。
- 新增 `launch/display.launch.py`，启动 `robot_state_publisher` 和 RViz2。
- 新增 `rviz/display.rviz`，正式保存 RobotModel + TF 的 RViz2 显示配置。
- 创建第 3 周第 2 小课讲义 `src/robot_description/WEEK_03_02_ROBOT_DESCRIPTION_URDF.md`。
- 新增 `test_robot_description_assets.py`，测试 `robot_description` 包结构、安装声明、依赖声明和 URDF link/joint 关系。
- 更新 `README.md` 和 `ros2_learning_notes.md`，加入第 3 周第 2 小课入口。
- 为 `diffbot.urdf` 补充教学注释，覆盖 `robot/link/joint/visual/collision/inertial/origin/geometry/material/mass/inertia/axis` 等 URDF 常见字段。
- 将 `robot_description` 的 RViz RobotModel 描述 topic QoS 改为 `Durability Policy: Transient Local`，避免 RViz 错过 `/robot_description`。
- 将第 1 周和第 3 周第 1 小课的“知识问答”统一为“问题 N / 参考答案”格式，第 3 周第 2 小课已保持该格式。
- 用户安装并验证 `ros-jazzy-xacro`，`ros2 pkg prefix xacro` 输出 `/opt/ros/jazzy`。
- 新增 `src/robot_description/urdf/diffbot.urdf.xacro`，作为第 3 周第 3 小课顶层 Xacro 模型。
- 新增 `src/robot_description/urdf/diffbot_materials.xacro`，集中定义 `body_blue`、`wheel_dark`、`camera_green`、`laser_red` 材质。
- 新增 `src/robot_description/urdf/diffbot_components.xacro`，集中定义左右轮、摄像头和雷达组件宏。
- 更新 `src/robot_description/launch/display.launch.py`，通过 `xacro.process_file()` 从 `diffbot.urdf.xacro` 生成 `robot_description`。
- 更新 `src/robot_description/setup.py` 和 `package.xml`，安装 `*.xacro` 并声明 `xacro` 运行依赖。
- 新增 `src/robot_bringup/launch/display_robot.launch.py`，include `robot_description/launch/display.launch.py`，作为推荐模型显示入口。
- 更新 `src/robot_bringup/package.xml`，声明对 `robot_description` 的运行依赖。
- 创建第 3 周第 3 小课讲义 `src/robot_description/WEEK_03_03_XACRO_AND_BRINGUP.md`。
- 更新 `README.md`、`ros2_learning_notes.md`、`src/robot_description/README.md` 和 `src/robot_bringup/README.md`，加入 Xacro 与 bringup 显示入口说明。
- 扩展 `test_robot_description_assets.py` 和 `test_bringup_assets.py`，覆盖 Xacro 文件、依赖、launch 处理和 bringup include 入口。
- 创建 ROS 2 Python 资源包 `src/robot_simulation`，用于第 4 周 Gazebo 仿真资产。
- 新增 `src/robot_simulation/worlds/empty_diffbot.world.sdf`，作为 Gazebo 空世界，包含物理、用户命令、场景广播插件、光源和地面。
- 新增 `src/robot_simulation/config/clock_bridge.yaml`，将 Gazebo `/clock` 单向桥接到 ROS 2 `/clock`。
- 新增 `src/robot_simulation/launch/gazebo_empty_world.launch.py`，include `ros_gz_sim/gz_sim.launch.py` 并启动 `ros_gz_bridge/parameter_bridge`。
- 创建第 4 周第 1 小课讲义 `src/robot_simulation/WEEK_04_01_GAZEBO_ENVIRONMENT.md`。
- 更新 `README.md` 和 `ros2_learning_notes.md`，加入第 4 周 Gazebo 环境检查、安装、空世界启动和 `/clock` 检查步骤。
- 新增 `src/robot_simulation/worlds/diffbot_drive.world.sdf`，在 Gazebo SDF world 中定义可运动差速小车模型。
- 新增 `src/robot_simulation/config/diff_drive_bridge.yaml`，桥接 `/clock`、ROS->Gazebo `/cmd_vel` 和 Gazebo->ROS `/odom`。
- 新增 `src/robot_simulation/launch/diffbot_drive.launch.py`，启动差速小车 world 和 bridge。
- 创建第 4 周第 2 小课讲义 `src/robot_simulation/WEEK_04_02_DIFFBOT_DRIVE_IN_GAZEBO.md`。
- 更新 `README.md`、`ros2_learning_notes.md` 和 `src/robot_simulation/README.md`，加入第二课运行和验证步骤。
- 新增 `src/robot_simulation/worlds/diffbot_sensors.world.sdf`，在 Gazebo 小车上加入 `laser_link`、`camera_link`、`front_lidar`、`front_camera` 和两个障碍物。
- 新增 `src/robot_simulation/config/sensor_bridge.yaml`，桥接 `/clock`、`/cmd_vel`、`/odom`、`/scan`、`/camera/image_raw` 和 `/camera/camera_info`。
- 新增 `src/robot_simulation/robot_simulation/odom_to_tf.py`，把 `/odom` 转成 `odom -> base_link` 动态 TF。
- 新增 `src/robot_simulation/rviz/sensors.rviz`，RViz 默认显示 RobotModel、TF、LaserScan 和相机图像，Fixed Frame 为 `odom`。
- 新增第 4 周第 3 小课讲义 `src/robot_simulation/WEEK_04_03_SENSORS_TF_RVIZ.md`。
- 更新 `README.md`、`ros2_learning_notes.md` 和 `src/robot_simulation/README.md`，加入第三课运行步骤和键盘 teleop 说明。
- 扩展 `src/robot_simulation/test/test_simulation_assets.py` 并新增 `src/robot_simulation/test/test_odom_to_tf.py`，覆盖第三课资产和 odom->TF 转换。
- 已删除不可用的 `diffbot_keyboard_teleop.launch.py` 方案；键盘控制统一用第二终端直接运行 `ros2 run teleop_twist_keyboard teleop_twist_keyboard`。
- 将 `diffbot_drive.world.sdf` 和 `diffbot_sensors.world.sdf` 中的小车支撑从单后 caster 改为 `front_caster_link` + `rear_caster_link`，避免 Gazebo 原地转向时绕轮轴翘起。

Important decisions:

- 学习环境建议使用 Ubuntu 24.04 + ROS 2 Jazzy。
- 第一个练习只做 turtlesim P 控制，不引入 Gazebo/Nav2，降低第一周复杂度。
- 控制数学与 ROS 2 节点分离，原因是数学逻辑可以在没有 ROS 2 的环境中验证。
- 文档命名规则：整周课件使用 `WEEK_01_...`；第二周起的小课使用 `WEEK_02_01_...`、`WEEK_02_02_...`。
- 后续每一课都要配套练习题、观察问题、知识问答、参考答案和验收标准。
- 后续每一课结束时必须同步更新 `ros2_learning_notes.md` 的正文学习笔记；不能只更新顶部进度或 README。
- 第 2 周第 1 小课先在原 `turtlesim_p_controller` 包内学习 launch/config，暂不新建 `robot_bringup`；后续小课再迁移到 bringup 包，降低概念密度。
- launch/config 是运行时资产，必须通过 `setup.py` 的 `data_files` 安装到 `install/<package>/share/<package>/`，否则 `ros2 launch` 找不到。
- 第 2 周调整为 3 节课：第 1 节 launch 与参数 YAML；第 2 节 `robot_bringup` 与工作空间组织；第 3 节自定义接口与综合练习。
- `robot_bringup` 当前不放控制算法和参数 YAML，只负责启动编排；控制器默认参数继续归属 `turtlesim_p_controller/config/goal_controller.yaml`。
- `robot_interfaces` 是纯接口包，使用 `ament_cmake` 和 `rosidl_generate_interfaces`；不放节点、不放 launch。
- 第 3 节让 `SetGoal.srv` 真正接入控制器；`TargetDetection.msg` 暂时用 CLI 模拟发布，为后续 YOLO 接入做概念准备。
- 第 3 周第 1 小课先单独创建 `tf2_frame_demo`，不把 tf2 示例塞进 `turtlesim_p_controller`；原因是 tf2 是系统级坐标关系，独立包更适合衔接后续 `robot_description`、URDF 和 RViz。
- 本课 TF 树固定为 `map -> odom -> base_link -> camera_link`，其中 `map -> odom` 和 `base_link -> camera_link` 是静态 transform，`odom -> base_link` 是动态 transform。
- 本课暂不引入 URDF；先用 `static_transform_publisher`、`TransformBroadcaster`、`TransformListener`、`tf2_echo` 和 RViz2 的 TF display 理解 frame/transform/TF 树。
- 第 1 小课的 RViz2 配置只用于临时观察，关闭时选择 `Discard`；正式可复用配置后续保存到 `robot_description/rviz/display.rviz`。
- `robot_description` 使用 `ament_python` 资源包风格，包内不放控制算法节点，只安装 launch、URDF、RViz 配置和讲义。
- 当前环境没有安装 `joint_state_publisher` / `joint_state_publisher_gui`；第 3 周第 2 小课先把轮子、摄像头和雷达都建模为 `fixed` joint，重点理解 URDF 如何生成固定 frame。轮子真实旋转和 `/joint_states` 后续在 Gazebo/控制课再引入。
- `camera_optical_frame` 通过 `camera_optical_joint` 挂在 `camera_link` 下，用于提前建立相机光学坐标系概念。
- 继续保留 RViz RobotModel 的 `Description Source: Topic`，因为它更贴近真实 ROS 2 链路：URDF -> `robot_state_publisher` -> `/robot_description` + `/tf_static` -> RViz。
- `diffbot.urdf` 保留为第 3 周第 2 小课普通 URDF 对照文件；第 3 周第 3 小课开始，运行入口默认使用 `diffbot.urdf.xacro` 生成模型。
- Xacro 文件拆分为顶层模型、材质、组件宏三类，避免一开始引入更深目录层级导致安装和 include 路径复杂化。
- `robot_bringup/display_robot.launch.py` 通过 include 复用 `robot_description/display.launch.py`，不复制 `robot_state_publisher` 和 RViz2 节点配置，保持模型显示细节归属 `robot_description`。
- 已按用户提醒补齐 `ros2_learning_notes.md` 的第 3 周第 1/2/3 小课正文学习笔记；后续进入第 4 周时继续按这个标准维护。
- 第 4 周新增 `robot_simulation` 包，职责只覆盖 Gazebo world、bridge 配置和仿真 launch；URDF/Xacro 继续归 `robot_description`，统一系统入口后续再由 `robot_bringup` include。
- 第 4 周第 1 小课先只桥接 `/clock`，不放机器人、不接 `/cmd_vel`、`/odom`、`/scan` 或相机，目的是先确认 Gazebo 与 ROS 2 的最小通信链路。
- 用户已安装 `ros-jazzy-ros-gz`；当前环境可发现 `gz`、`ros_gz_sim` 和 `ros_gz_bridge`。
- 第 4 周第 2 小课先用 SDF 直接定义 Gazebo 可动小车，暂不从 `robot_description` 的 URDF/Xacro 生成 Gazebo 模型；原因是本课重点是物理 joint、DiffDrive 插件和 bridge 方向。
- 第 4 周第 2 小课只桥接 `/cmd_vel` 与 `/odom`，不引入雷达、相机或 RViz；这些留到第 4 周第 3 小课，避免一次引入过多链路。
- 第 4 周第 2 小课采用 `x` 向前、`y` 向左、`z` 向上的常见 ROS 坐标约定；左右轮轴沿 `y` 方向，因此 `left_wheel_joint` 和 `right_wheel_joint` 的 `<axis><xyz>` 固定为 `0 1 0`。wheel link 本身不 roll，只有 visual/collision 圆柱局部 pose 使用 `1.5708 0 0` 把 cylinder 轴转到 `y` 方向。
- 第 4 周第 3 小课继续使用单独 SDF world 承载 Gazebo 传感器；`robot_description` 的 Xacro 用于 ROS 侧 `robot_state_publisher` 发布固定 TF 和 RobotModel，不作为本课 Gazebo 模型来源。
- `/odom` 不等于 `/tf`；新增 `odom_to_tf` 节点专门发布 `odom -> base_link`，传感器固定 frame 仍由 `robot_state_publisher` 发布。
- `teleop_twist_keyboard` 需要真实交互终端 stdin，不能包装进普通 `ros2 launch`；课程中固定用第二终端直接 `ros2 run teleop_twist_keyboard teleop_twist_keyboard`。
- Gazebo 物理稳定性要看 collision、inertial 和接地点支撑区域；RViz 姿态正常不代表 Gazebo 小车不会翻。第 4 周小车使用前后两个 caster 扩大支撑区域。

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
- 已运行 `source /opt/ros/jazzy/setup.bash && PYTHONPATH=src/tf2_frame_demo:$PYTHONPATH python3 -m unittest discover -s src/tf2_frame_demo/test`，10 个测试通过。
- 已运行 `python3 -m compileall src/tf2_frame_demo/tf2_frame_demo src/tf2_frame_demo/launch src/tf2_frame_demo/test`，语法检查通过。
- 已运行 `source /opt/ros/jazzy/setup.bash && colcon build --packages-select tf2_frame_demo`，构建通过。
- 已运行 `ros2 pkg executables tf2_frame_demo`，确认入口为 `dynamic_frame_broadcaster` 和 `frame_listener`。
- 已运行 `ros2 launch tf2_frame_demo tf2_demo.launch.py --show-args`，在 `ROS_LOG_DIR=/tmp/ros2_launch_logs` 下确认 launch 文件可被加载。
- 已用 `timeout 8s ros2 launch tf2_frame_demo tf2_demo.launch.py` 短时启动验证，listener 打印了连续变化的 `map -> camera_link`。
- 已用 `timeout -s INT 7s ros2 launch tf2_frame_demo tf2_demo.launch.py` 模拟 Ctrl-C，确认两个 Python 节点 clean exit。
- 已运行 `python3 -m unittest discover -s src/robot_description/test`，7 个测试通过。
- 已运行 `python3 -m compileall src/robot_description`，语法检查通过。
- 已运行 `source /opt/ros/jazzy/setup.bash && check_urdf src/robot_description/urdf/diffbot.urdf`，URDF 解析通过，根 link 为 `base_link`，有 4 个直接子 link。
- 已运行 `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_description`，构建通过。
- 已运行 `ROS_LOG_DIR=/tmp/ros2_launch_logs ros2 launch robot_description display.launch.py --show-args`，确认 launch 文件可被加载。
- 已运行 `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_interfaces turtlesim_p_controller robot_bringup tf2_frame_demo robot_description`，5 个包构建通过。
- 已实际运行 turtlesim 图形窗口和控制器节点。
- 已使用 `/reset` 服务验证 service 调用。
- 已使用 rqt_graph 观察 `/turtlesim` 和 `/turtle_goal_controller` 的 topic 连接关系。
- 已运行 `source /opt/ros/jazzy/setup.bash && python3 -m unittest discover -s src/robot_description/test`，8 个测试通过。
- 已运行 `python3 -m unittest discover -s src/robot_bringup/test`，4 个测试通过。
- 已运行 `python3 -m compileall src/robot_description src/robot_bringup`，语法检查通过。
- 已运行 `source /opt/ros/jazzy/setup.bash && xacro src/robot_description/urdf/diffbot.urdf.xacro -o /tmp/diffbot_from_xacro.urdf`，Xacro 展开成功。
- 已运行 `source /opt/ros/jazzy/setup.bash && check_urdf /tmp/diffbot_from_xacro.urdf`，URDF 解析通过，根 link 为 `base_link`，有 4 个直接子 link。
- 已运行 `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_description robot_bringup`，两个包构建通过。
- 已运行 `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ROS_LOG_DIR=/tmp/ros2_launch_logs ros2 launch robot_description display.launch.py --show-args`，确认模型包 launch 可加载。
- 已运行 `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ROS_LOG_DIR=/tmp/ros2_launch_logs ros2 launch robot_bringup display_robot.launch.py --show-args`，确认 bringup 入口 launch 可加载。
- 已运行 `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_interfaces turtlesim_p_controller robot_bringup tf2_frame_demo robot_description`，5 个包构建通过。
- 已运行 `git diff --check`，无空白错误。
- 已按 TDD 先新增 `src/robot_simulation/test/test_simulation_assets.py`，首次运行 `python3 -m unittest discover -s src/robot_simulation/test` 失败 6 项，失败原因均为目标资产不存在。
- 已补齐 `robot_simulation` 包后重新运行 `python3 -m unittest discover -s src/robot_simulation/test`，6 个测试通过。
- 已运行 `python3 -m unittest discover -s src/robot_bringup/test`，4 个测试通过。
- 已运行 `source /opt/ros/jazzy/setup.bash && PYTHONPATH=src/robot_description:$PYTHONPATH python3 -m unittest discover -s src/robot_description/test`，8 个测试通过。
- 已运行 `python3 -m compileall src/robot_simulation src/robot_bringup`，语法检查通过。
- 已运行 `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_interfaces turtlesim_p_controller robot_bringup tf2_frame_demo robot_description robot_simulation`，6 个包构建通过。
- 已运行 `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ros2 pkg prefix robot_simulation`，确认新包可发现。
- 安装 `ros-jazzy-ros-gz` 后，已运行 `source /opt/ros/jazzy/setup.bash && command -v gz && ros2 pkg prefix ros_gz_sim && ros2 pkg prefix ros_gz_bridge`，确认 `gz=/opt/ros/jazzy/opt/gz_tools_vendor/bin/gz`，两个 ROS 包均在 `/opt/ros/jazzy`。
- 已运行 `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ROS_LOG_DIR=/tmp/ros2_launch_logs ros2 launch robot_simulation gazebo_empty_world.launch.py --show-args`，launch 参数可正常显示。
- 已实际启动 `ros2 launch robot_simulation gazebo_empty_world.launch.py`，Gazebo 和 `parameter_bridge` 进程启动，日志显示创建 `[/clock (gz.msgs.Clock) -> /clock (rosgraph_msgs/msg/Clock)]`。
- 已运行 `source /opt/ros/jazzy/setup.bash && source install/setup.bash && timeout 10s ros2 topic echo /clock --once`，成功输出仿真时间，例如 `sec: 255`。
- 已运行 `source /opt/ros/jazzy/setup.bash && gz topic -l | head -40`，能看到 `/world/diffbot_empty_world/...` 和 `/clock` 等 Gazebo Transport topic。
- 已运行 `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ros2 node list --no-daemon`，能看到 `/clock_bridge`。
- 已运行 `source /opt/ros/jazzy/setup.bash && source install/setup.bash && timeout 10s ros2 topic info /clock --verbose --no-daemon`，确认 `/clock` 的 publisher 为 `clock_bridge`，类型为 `rosgraph_msgs/msg/Clock`。
- 已运行 `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ros2 topic list | sort | grep -E "^/clock$|^/parameter_events$|^/rosout$"`，能看到 `/clock`。
- 第 4 周第 2 小课 TDD RED：扩展 `src/robot_simulation/test/test_simulation_assets.py` 后运行 `python3 -m unittest discover -s src/robot_simulation/test`，失败 5 项，原因包括 `diffbot_drive.world.sdf`、`diff_drive_bridge.yaml`、`diffbot_drive.launch.py`、第二课讲义和消息依赖不存在。
- 第 4 周第 2 小课 GREEN：补齐资产后运行 `python3 -m unittest discover -s src/robot_simulation/test`，9 个测试通过。
- 已运行 `python3 -m compileall src/robot_simulation`，语法检查通过。
- 已运行 `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_simulation`，构建通过。
- 已运行 `git diff --check`，无空白错误。
- 已运行 `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ROS_LOG_DIR=/tmp/ros2_launch_logs ros2 launch robot_simulation diffbot_drive.launch.py --show-args`，launch 参数可正常显示。
- 已运行 `source /opt/ros/jazzy/setup.bash && gz sdf -k src/robot_simulation/worlds/diffbot_drive.world.sdf`，SDF 输出 `Valid.`。
- 已实际启动 `ros2 launch robot_simulation diffbot_drive.launch.py`，日志显示 bridge 创建 `/clock`、`/cmd_vel`、`/odom` 三条链路。
- 已运行 `ros2 topic list | sort | grep -E "^/clock$|^/cmd_vel$|^/odom$"`，确认 ROS 侧有 `/clock`、`/cmd_vel` 和 `/odom`。
- 已运行 `gz topic -l | grep -E "^/cmd_vel$|^/odom$|diffbot_drive_world"`，确认 Gazebo 侧有 `/cmd_vel`、`/odom` 和 `diffbot_drive_world` 相关 topic。
- 已运行 `timeout 10s ros2 topic echo /odom --once`，初始 `position.x` 近似 0，`frame_id=odom`，`child_frame_id=base_link`。
- 已运行 `timeout 4s ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.25}, angular: {z: 0.0}}"` 发布前进命令，然后发布停止命令。
- 运动后再次运行 `timeout 10s ros2 topic echo /odom --once`，`position.x` 约为 `6.7435`，证明小车响应 `/cmd_vel` 且 `/odom` 回传有效。
- 用户指出轮子不应绕 `z` 轴转；已核对当前 SDF 使用 `0 1 0`，并在 `test_simulation_assets.py` 增加断言锁定左右轮 joint axis 为 `0 1 0`。
- 用户进一步指出 Gazebo 视觉中轮子像“平着转”；已确认原写法把 wheel link 自身 roll `1.5708`，容易让 link frame 和几何姿态混在一起。已改为 wheel link pose 不旋转，visual/collision 圆柱局部 pose 使用 `1.5708 0 0`，用户目视确认修正后轮子姿态正确。
- 已重新运行 `python3 -m unittest discover -s src/robot_simulation/test`，9 个测试通过。
- 已重新运行 `python3 -m compileall src/robot_simulation`，语法检查通过。
- 已重新运行 `source /opt/ros/jazzy/setup.bash && gz sdf -k src/robot_simulation/worlds/diffbot_drive.world.sdf`，输出 `Valid.`。
- 已重新运行 `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_simulation`，构建通过。
- 已停止验证用 Gazebo launch，`parameter_bridge` clean exit。
- 第 4 周第 3 小课 TDD RED：扩展资产测试并新增 `test_odom_to_tf.py` 后运行 `source /opt/ros/jazzy/setup.bash && PYTHONPATH=src/robot_simulation:$PYTHONPATH python3 -m unittest discover -s src/robot_simulation/test`，失败 9 项，原因均为第三课资产或 `odom_to_tf` 不存在。
- 第 4 周第 3 小课 GREEN：补齐资产后重新运行同一测试命令，15 个测试通过。
- 已运行 `python3 -m compileall src/robot_simulation`，语法检查通过。
- 已运行 `source /opt/ros/jazzy/setup.bash && gz sdf -k src/robot_simulation/worlds/diffbot_sensors.world.sdf`，输出 `Valid.`。
- 已运行 `git diff --check`，无空白错误。
- 已运行 `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_description robot_simulation`，两个包构建通过。
- 已运行 `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ROS_LOG_DIR=/tmp/ros2_launch_logs ros2 launch robot_simulation diffbot_sensors_rviz.launch.py --show-args`，主 launch 可加载。
- 已运行 `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ros2 pkg executables robot_simulation`，确认入口为 `odom_to_tf`。
- 已运行安装环境下的 `odometry_to_transform` 导入和转换检查，输出 `odom base_link 2.0`。
- 已运行 `source /opt/ros/jazzy/setup.bash && source install/setup.bash && xacro src/robot_description/urdf/diffbot.urdf.xacro -o /tmp/diffbot_week4_03.urdf && check_urdf /tmp/diffbot_week4_03.urdf`，URDF 解析通过。
- 已在 PTY 中短时运行 `ros2 run teleop_twist_keyboard teleop_twist_keyboard`，进入键盘说明界面；当前沙箱仍有 DDS socket 权限噪声，但没有 `termios` 错误。
- 已短时启动 `diffbot_sensors_rviz.launch.py`，确认 Gazebo、bridge、`robot_state_publisher`、`odom_to_tf` 和 RViz 进程均被创建；受当前沙箱无 GUI、DDS socket 限制和 `/home/sheepyjb/.gz` 日志写入限制影响，未完成完整 GUI/话题实机验证。
- 用户反馈 Gazebo 中小车翘起后，已用 headless Gazebo 复现：静止和直行基本水平，持续原地转向后旧单后 caster 模型出现明显 pitch/roll。
- caster 修复后已重新运行 `source /opt/ros/jazzy/setup.bash && PYTHONPATH=src/robot_simulation:$PYTHONPATH python3 -m unittest discover -s src/robot_simulation/test`，15 个测试通过。
- caster 修复后已重新运行 `python3 -m compileall src/robot_simulation`，语法检查通过。
- caster 修复后已重新运行 `source /opt/ros/jazzy/setup.bash && gz sdf -k src/robot_simulation/worlds/diffbot_drive.world.sdf` 和 `source /opt/ros/jazzy/setup.bash && gz sdf -k src/robot_simulation/worlds/diffbot_sensors.world.sdf`，均输出 `Valid.`。
- caster 修复后已重新运行 `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_simulation`，构建通过。
- caster 修复后已重新运行 `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ROS_LOG_DIR=/tmp/ros2_launch_logs ros2 launch robot_simulation diffbot_sensors_rviz.launch.py --show-args`，主 launch 可加载。
- caster 修复后已运行 headless Gazebo 原地转向验证：转向后 `diffbot` orientation 的 `x=-1.092e-07`、`y=1.690e-07`，只剩 yaw 分量明显变化，没有再绕轮轴翘起。
- 已运行 `git diff --check`，无空白错误。

Remaining tasks:

- 第 5 周开始接入 YOLO 图像处理链路。

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
- `src/tf2_frame_demo/WEEK_03_01_TF2_FRAMES.md`
- `src/tf2_frame_demo/launch/tf2_demo.launch.py`
- `src/tf2_frame_demo/tf2_frame_demo/frame_math.py`
- `src/tf2_frame_demo/tf2_frame_demo/dynamic_frame_broadcaster.py`
- `src/tf2_frame_demo/tf2_frame_demo/frame_listener.py`
- `src/tf2_frame_demo/test/test_frame_math.py`
- `src/tf2_frame_demo/test/test_tf2_frame_demo_assets.py`
- `src/tf2_frame_demo/test/test_node_shutdown.py`
- `src/robot_description/WEEK_03_02_ROBOT_DESCRIPTION_URDF.md`
- `src/robot_description/WEEK_03_03_XACRO_AND_BRINGUP.md`
- `src/robot_description/launch/display.launch.py`
- `src/robot_description/urdf/diffbot.urdf`
- `src/robot_description/urdf/diffbot.urdf.xacro`
- `src/robot_description/urdf/diffbot_materials.xacro`
- `src/robot_description/urdf/diffbot_components.xacro`
- `src/robot_description/rviz/display.rviz`
- `src/robot_description/package.xml`
- `src/robot_description/setup.py`
- `src/robot_description/test/test_robot_description_assets.py`
- `src/robot_bringup/launch/display_robot.launch.py`
- `src/robot_simulation/WEEK_04_01_GAZEBO_ENVIRONMENT.md`
- `src/robot_simulation/launch/gazebo_empty_world.launch.py`
- `src/robot_simulation/worlds/empty_diffbot.world.sdf`
- `src/robot_simulation/config/clock_bridge.yaml`
- `src/robot_simulation/WEEK_04_02_DIFFBOT_DRIVE_IN_GAZEBO.md`
- `src/robot_simulation/launch/diffbot_drive.launch.py`
- `src/robot_simulation/worlds/diffbot_drive.world.sdf`
- `src/robot_simulation/config/diff_drive_bridge.yaml`
- `src/robot_simulation/config/sensor_bridge.yaml`
- `src/robot_simulation/launch/diffbot_sensors_rviz.launch.py`
- `src/robot_simulation/robot_simulation/odom_to_tf.py`
- `src/robot_simulation/rviz/sensors.rviz`
- `src/robot_simulation/worlds/diffbot_sensors.world.sdf`
- `src/robot_simulation/WEEK_04_03_SENSORS_TF_RVIZ.md`
- `src/robot_simulation/package.xml`
- `src/robot_simulation/setup.py`
- `src/robot_simulation/test/test_simulation_assets.py`
- `src/robot_simulation/test/test_odom_to_tf.py`

## Session Notes

### 2026-06-16

- Progress/result checkpoint:
  - 用户在桌面终端实际运行第 4 周第 3 小课后确认 Gazebo/RViz 已正常，之前小车翘起问题已解决。
  - 第 4 周整体已完成，准备提交本次课程改动。
- Verification:
  - 本次提交前重新运行关键验证，结果记录在 Latest Snapshot 的 Verification 区域。
- Next:
  - 提交后进入第 5 周 YOLO 图像链路。

### 2026-06-14

- Progress/result checkpoint:
  - 用户开始第 4 周第 3 小课，并指出键盘控制小车运动必须补上。
  - 已完成第三课：`diffbot_sensors.world.sdf`、`sensor_bridge.yaml`、`diffbot_sensors_rviz.launch.py`、`odom_to_tf.py`、`sensors.rviz`、讲义和 README/总笔记更新。
  - 已将键盘控制定为第二终端直接运行 `ros2 run teleop_twist_keyboard teleop_twist_keyboard`；验证普通 launch 启动 teleop 会触发 `termios.error`，已删除该 launch 方案并写入 `CODEX_PITFALLS.md`。
  - 第三课主链路为：键盘 `/cmd_vel` -> Gazebo DiffDrive -> `/odom` -> `odom_to_tf` -> RViz，同时桥接 `/scan`、`/camera/image_raw` 和 `/camera/camera_info`。
  - 用户上传截图指出 Gazebo 中小车会翘起，而 RViz 中正常。已确认这不是 RViz 显示问题，而是 Gazebo SDF 物理支撑问题。
  - 根因是左右驱动轮加单后 caster 的支撑区域太小，前边界接近轮轴；传感器加到车体后，原地转向容易产生 pitch/roll。
  - 已将 `diffbot_drive.world.sdf` 和 `diffbot_sensors.world.sdf` 改为前后两个 caster：`front_caster_link` 位于 `x=0.16`，`rear_caster_link` 位于 `x=-0.16`。
- Verification:
  - RED：`source /opt/ros/jazzy/setup.bash && PYTHONPATH=src/robot_simulation:$PYTHONPATH python3 -m unittest discover -s src/robot_simulation/test` 失败 9 项，原因是第三课目标资产和 `odom_to_tf` 尚不存在。
  - GREEN：同一测试命令通过 15 个测试。
  - `python3 -m compileall src/robot_simulation` 通过。
  - `source /opt/ros/jazzy/setup.bash && gz sdf -k src/robot_simulation/worlds/diffbot_sensors.world.sdf` 输出 `Valid.`。
  - `git diff --check` 通过。
  - `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_description robot_simulation` 通过。
  - `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ROS_LOG_DIR=/tmp/ros2_launch_logs ros2 launch robot_simulation diffbot_sensors_rviz.launch.py --show-args` 通过。
  - `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ros2 pkg executables robot_simulation` 输出 `robot_simulation odom_to_tf`。
  - 安装环境下导入 `odometry_to_transform` 并转换测试消息，输出 `odom base_link 2.0`。
  - `source /opt/ros/jazzy/setup.bash && source install/setup.bash && xacro src/robot_description/urdf/diffbot.urdf.xacro -o /tmp/diffbot_week4_03.urdf && check_urdf /tmp/diffbot_week4_03.urdf` 通过。
  - PTY 中直接运行 `ros2 run teleop_twist_keyboard teleop_twist_keyboard` 能进入键盘说明界面，无 `termios` 错误。
  - 当前沙箱无法完整 GUI 实机验证：RViz 无显示器、Gazebo 不能写 `~/.gz` 日志、DDS socket 权限受限。
  - caster 修复后补充验证：15 个 `robot_simulation` 测试通过，`compileall` 通过，`gz sdf -k` 两个 world 均 `Valid.`，`colcon build --packages-select robot_simulation` 通过，主 launch `--show-args` 通过。
  - caster 修复后 headless Gazebo 原地转向验证通过：转向后 `orientation.x/y` 保持在 `1e-7` 量级，未再出现明显 pitch/roll。
- Next:
  - 用户可在正常桌面终端运行第三课两个终端流程并目视确认 Gazebo/RViz 同步。
  - 下一课进入第 5 周 YOLO 图像链路。

### 2026-06-12

- Progress/result checkpoint:
  - 用户要求提交第 4 周第 1 小课并开始第二课。
  - 已提交第 4 周第 1 小课，提交 `6755c39 Add week 4 Gazebo environment lesson`。
  - 已完成第 4 周第 2 小课：可运动差速小车 Gazebo world、DiffDrive 插件、`/cmd_vel` 和 `/odom` bridge、课程讲义和总文档更新。
  - 第二课采用直接 SDF 小车，不复用第 3 周 URDF/Xacro；该决策已记录为本课边界。
  - 已记录 SDF `<canonical_link>` 警告和 install 资产需重建的坑点到 `CODEX_PITFALLS.md`。
- Verification:
  - `python3 -m unittest discover -s src/robot_simulation/test` RED 阶段失败 5 项，随后 GREEN 阶段通过 9 个测试。
  - `python3 -m compileall src/robot_simulation` 通过。
  - `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_simulation` 通过。
  - `git diff --check` 通过。
  - `ros2 launch robot_simulation diffbot_drive.launch.py --show-args` 通过。
  - `gz sdf -k src/robot_simulation/worlds/diffbot_drive.world.sdf` 输出 `Valid.`。
  - 实际启动 `ros2 launch robot_simulation diffbot_drive.launch.py` 后，bridge 日志显示 `/clock` GZ->ROS、`/cmd_vel` ROS->GZ、`/odom` GZ->ROS 三条链路创建成功。
  - `ros2 topic list` 能看到 `/clock`、`/cmd_vel`、`/odom`。
  - `gz topic -l` 能看到 `/cmd_vel`、`/odom` 和 `/world/diffbot_drive_world/...`。
  - 初始 `/odom` 的 `position.x` 近似 0；发布 `/cmd_vel` 前进命令后，`/odom` 的 `position.x` 约为 `6.7435`，并已发送停止命令。
  - 用户质疑轮子轴向，已确认本课 SDF 中轮子 joint axis 是 `0 1 0` 而不是 `0 0 1`；讲义已补充解释，并用测试断言锁定。
  - 用户继续指出轮子视觉姿态像平着转；已将 wheel link pose 从 `0 +/-0.18 0.07 1.5708 0 0` 改为 `0 +/-0.18 0.07 0 0 0`，并把 `1.5708 0 0` 放到 wheel visual/collision 的局部 pose。用户确认“现在是对的了”。
  - 轴向说明补充后，`python3 -m unittest discover -s src/robot_simulation/test`、`python3 -m compileall src/robot_simulation`、`gz sdf -k src/robot_simulation/worlds/diffbot_drive.world.sdf` 和 `colcon build --packages-select robot_simulation` 均通过。
- Next:
  - 第 4 周第 3 小课：接入雷达、相机、TF 和 RViz。

### 2026-06-12

- Progress/result checkpoint:
  - 用户确认开始第 4 周 Gazebo。
  - 已创建 `robot_simulation` 包，并完成第 4 周第 1 小课：Gazebo Harmonic 与 `ros_gz` 最小链路。
  - 新增空世界 `empty_diffbot.world.sdf`、`/clock` bridge 配置 `clock_bridge.yaml`、启动入口 `gazebo_empty_world.launch.py` 和讲义 `WEEK_04_01_GAZEBO_ENVIRONMENT.md`。
  - 已更新 `README.md` 和 `ros2_learning_notes.md`，延续每课同步总学习笔记的要求。
  - 当前机器最初未安装 `gz`、`ros_gz_sim`、`ros_gz_bridge`；用户已在终端安装 `ros-jazzy-ros-gz`，随后完成实际 Gazebo 验证。
- Verification:
  - TDD RED：`python3 -m unittest discover -s src/robot_simulation/test` 首次失败 6 项，原因均为资产不存在。
  - GREEN：`python3 -m unittest discover -s src/robot_simulation/test` 通过，6 个测试。
  - `python3 -m unittest discover -s src/robot_bringup/test` 通过，4 个测试。
  - `source /opt/ros/jazzy/setup.bash && PYTHONPATH=src/robot_description:$PYTHONPATH python3 -m unittest discover -s src/robot_description/test` 通过，8 个测试。
  - `python3 -m compileall src/robot_simulation src/robot_bringup` 通过。
  - `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_interfaces turtlesim_p_controller robot_bringup tf2_frame_demo robot_description robot_simulation` 通过，6 个包。
  - `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ros2 pkg prefix robot_simulation` 输出 `/home/sheepyjb/ros/install/robot_simulation`。
  - 安装前 `ros2 launch robot_simulation gazebo_empty_world.launch.py --show-args` 失败于缺 `ros_gz_sim`，不是新包构建失败。
  - 安装后 `command -v gz` 输出 `/opt/ros/jazzy/opt/gz_tools_vendor/bin/gz`，`ros2 pkg prefix ros_gz_sim` 和 `ros2 pkg prefix ros_gz_bridge` 均输出 `/opt/ros/jazzy`。
  - 安装后 `ros2 launch robot_simulation gazebo_empty_world.launch.py --show-args` 通过。
  - 实际启动 Gazebo 后，launch 日志显示 `clock_bridge` 创建 `GZ->ROS Bridge: [/clock (gz.msgs.Clock) -> /clock (rosgraph_msgs/msg/Clock)]`。
  - `ros2 topic echo /clock --once` 成功输出仿真时间。
  - `gz topic -l` 能看到 `/world/diffbot_empty_world/...` topic。
  - `ros2 node list --no-daemon` 能看到 `/clock_bridge`。
  - `ros2 topic info /clock --verbose --no-daemon` 确认 `/clock` 的 publisher 是 `clock_bridge`。
  - 默认 `ros2 topic list` 能看到 `/clock`、`/parameter_events` 和 `/rosout`。
- Next:
  - 进入第 4 周第 2 小课：把差速小车放入 Gazebo，加入差速驱动插件，桥接 `/cmd_vel` 和 `/odom`。

### 2026-06-12

- Progress/result checkpoint:
  - 用户安装 `ros-jazzy-xacro`，`ros2 pkg prefix xacro` 已可发现包；`xacro --version` 在当前 Jazzy 版本不支持，已在讲义中说明。
  - 第 3 周第 3 小课代码与讲义已准备完成：新增 Xacro 顶层模型、材质文件、组件宏文件和 bringup 模型显示入口。
  - `robot_description/display.launch.py` 已改为从 `diffbot.urdf.xacro` 生成 `robot_description`。
  - `robot_bringup/display_robot.launch.py` include `robot_description/display.launch.py`，推荐后续从 bringup 启动模型显示。
  - 已更新 README、总学习笔记、两个包 README 和本课测试。
- Verification:
  - `source /opt/ros/jazzy/setup.bash && python3 -m unittest discover -s src/robot_description/test` 通过，8 个测试。
  - `python3 -m unittest discover -s src/robot_bringup/test` 通过，4 个测试。
  - `python3 -m compileall src/robot_description src/robot_bringup` 通过。
  - `source /opt/ros/jazzy/setup.bash && xacro src/robot_description/urdf/diffbot.urdf.xacro -o /tmp/diffbot_from_xacro.urdf` 通过。
  - `source /opt/ros/jazzy/setup.bash && check_urdf /tmp/diffbot_from_xacro.urdf` 通过，根 link 为 `base_link`。
  - `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_interfaces turtlesim_p_controller robot_bringup tf2_frame_demo robot_description` 通过。
  - `ros2 launch robot_description display.launch.py --show-args` 和 `ros2 launch robot_bringup display_robot.launch.py --show-args` 均通过。
  - 用户提醒 `ros2_learning_notes.md` 正文学习笔记没有持续更新；已补齐第 3 周第 1/2/3 小课独立笔记，并记录为后续流程要求。
- Next:
  - 带用户运行 `ros2 launch robot_bringup display_robot.launch.py`，在 RViz2 中确认模型显示与上一课一致。
  - 带用户运行 `xacro src/robot_description/urdf/diffbot.urdf.xacro`、`tf2_echo base_link camera_link`、`tf2_echo base_link laser_link`，理解 Xacro 展开后仍是 URDF/TF。

### 2026-06-12

- Progress/result checkpoint:
  - 用户完成第 3 周第 2 小课实操：能在 RViz2 中观察 `robot_description` 生成的 RobotModel 和 TF。
  - 用户确认理解：红色圆柱为 `laser_link`，摄像头包含 `camera_link` 和 `camera_optical_frame` 两个 frame；二者原点重合但姿态不同。
  - 已为 `src/robot_description/urdf/diffbot.urdf` 补充中文教学注释，解释每类 URDF 标签和参数含义。
  - 已将 `src/robot_description/rviz/display.rviz` 的 RobotModel `/robot_description` topic Durability 改为 `Transient Local`。
  - 已把第 1 周和第 3 周第 1 小课的知识问答统一为第 3 周第 2 小课的格式：`问题 N：`、问题代码块、`参考答案：`、答案代码块。
  - 用户要求提交当前进度，并计划新建对话开始第 3 周第 3 小课。
- Verification:
  - `python3 -m unittest discover -s src/robot_description/test` 通过，当前 7 个测试。
  - `source /opt/ros/jazzy/setup.bash && check_urdf src/robot_description/urdf/diffbot.urdf` 通过。
  - `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_description` 通过。
  - `ROS_LOG_DIR=/tmp/ros2_launch_logs ros2 launch robot_description display.launch.py --show-args` 通过。
  - `source /opt/ros/jazzy/setup.bash && source install/setup.bash && ros2 topic info -v /robot_description --no-daemon` 在非沙箱环境确认 publisher/subscriber QoS 都是 `TRANSIENT_LOCAL`。
- Next:
  - 第 3 周第 3 小课从 Xacro 开始，建议将 `diffbot.urdf` 转成 `diffbot.urdf.xacro`，抽出尺寸参数、颜色/material、传感器安装宏，并把 `robot_bringup` 接入模型显示 launch。

### 2026-06-11

- Progress/result checkpoint:
  - 用户开始第 3 周第 2 小课：`robot_description`、URDF、轮子、摄像头和雷达 frame。
  - 已创建 `robot_description` 包，采用 `ament_python` 资源包结构。
  - 已创建 `diffbot.urdf`，模型树为 `base_link -> left_wheel_link/right_wheel_link/camera_link/laser_link`，并包含 `camera_link -> camera_optical_frame`。
  - 已创建 `display.launch.py`，启动 `robot_state_publisher` 和 RViz2；不依赖 `joint_state_publisher_gui`。
  - 已创建正式 RViz2 配置 `rviz/display.rviz`，显示 Grid、RobotModel 和 TF。
  - 已创建讲义 `WEEK_03_02_ROBOT_DESCRIPTION_URDF.md`，包含练习题、知识问答、参考答案和完成标准。
  - 已按用户提醒更新 `ros2_learning_notes.md`，并同步更新 `README.md`。
  - 发现当前环境没有 `joint_state_publisher` / `joint_state_publisher_gui`，已记录到 `CODEX_PITFALLS.md`。
- Verification:
  - `python3 -m unittest discover -s src/robot_description/test` 通过，当前 5 个测试。
  - `python3 -m compileall src/robot_description` 通过。
  - `source /opt/ros/jazzy/setup.bash && check_urdf src/robot_description/urdf/diffbot.urdf` 通过，root link 为 `base_link`。
  - `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_description` 通过。
  - `ROS_LOG_DIR=/tmp/ros2_launch_logs ros2 launch robot_description display.launch.py --show-args` 通过。
  - `source /opt/ros/jazzy/setup.bash && colcon build --packages-select robot_interfaces turtlesim_p_controller robot_bringup tf2_frame_demo robot_description` 通过。
- Next:
  - 带用户运行 `ros2 launch robot_description display.launch.py`，在 RViz2 中观察 RobotModel 和 TF。
  - 用 `tf2_echo base_link camera_link`、`tf2_echo base_link laser_link` 和 `view_frames` 检查模型 frame。
  - 确认用户能解释 URDF link/joint、fixed joint、`robot_state_publisher` 和 RobotModel/TF 的关系后，进入第 3 周第 3 小课 Xacro。

### 2026-06-10

- Progress/result checkpoint:
  - 用户开始第 3 周第 1 小课：tf2 与 ROS 2 坐标系入门。
  - 已创建 `tf2_frame_demo` 示例包和讲义 `WEEK_03_01_TF2_FRAMES.md`。
  - 示例 TF 树为 `map -> odom -> base_link -> camera_link`。
  - `map -> odom` 和 `base_link -> camera_link` 由 launch 中的 `tf2_ros/static_transform_publisher` 发布。
  - `odom -> base_link` 由 `dynamic_frame_broadcaster` 发布，`frame_listener` 查询 `map -> camera_link`。
  - 用户实操确认：launch 初期等待 TF，之后 listener 和 `tf2_echo map camera_link` 都能持续输出坐标变换。
  - 用户实操确认：RViz2 中添加 TF display 后能看到 `map/odom/base_link/camera_link`，其中 `base_link` 绕 `odom` 运动，`camera_link` 跟随 `base_link`。
  - 已按用户要求把 RViz2 可视化纳入第 3 周第 1 小课正式讲义；关闭 RViz2 时选择 `Discard`，不保存临时 `~/.rviz2/default.rviz`。
  - 已按用户要求给第 3 周第 1 小课核心代码补充详细教学注释：`frame_math.py`、`dynamic_frame_broadcaster.py`、`frame_listener.py`、`tf2_demo.launch.py`。
  - 已修复 Ctrl-C 退出时两个 Python 节点的 traceback；原因是 rclpy context 可能已由信号处理器 shutdown，代码又重复 shutdown。
- Verification:
  - `source /opt/ros/jazzy/setup.bash && PYTHONPATH=src/tf2_frame_demo:$PYTHONPATH python3 -m unittest discover -s src/tf2_frame_demo/test` 通过，当前 10 个测试。
  - `python3 -m compileall src/tf2_frame_demo/tf2_frame_demo src/tf2_frame_demo/launch src/tf2_frame_demo/test` 通过。
  - `source /opt/ros/jazzy/setup.bash && colcon build --packages-select tf2_frame_demo` 通过。
  - `ros2 pkg executables tf2_frame_demo` 显示 `dynamic_frame_broadcaster` 和 `frame_listener`。
  - `ROS_LOG_DIR=/tmp/ros2_launch_logs ros2 launch tf2_frame_demo tf2_demo.launch.py --show-args` 通过。
  - `timeout 8s ros2 launch tf2_frame_demo tf2_demo.launch.py` 能启动并打印变化的 `map -> camera_link`；沙箱中出现 DDS `Operation not permitted` 噪声，但节点仍完成 TF 查询。
  - `timeout -s INT 7s ros2 launch tf2_frame_demo tf2_demo.launch.py` 验证中，`frame_listener` 和 `dynamic_frame_broadcaster` 在 SIGINT 后均 clean exit；沙箱中 static_transform_publisher 显示 `exit code -2` 属于外部 SIGINT。
- Next:
  - 带用户完成第 3 周第 1 小课收尾问答，确认能解释父/子 frame、静态/动态 TF、TF 树间接查询和 RViz2 中看到的是坐标系而不是模型。
  - 用户理解后进入合并后的第 3 周第 2 小课：`robot_description`、URDF、轮子、摄像头和雷达 frame。

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
