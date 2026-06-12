# CODEX_PITFALLS

## 2026-06-12

Symptom:

- `README.md` 和课程讲义已更新，但 `ros2_learning_notes.md` 只更新了顶部进度，没有补充对应小课的正文学习笔记，用户在 VS Code 中发现总笔记缺失。

Root cause:

- 结束课程时只检查了入口说明和交接记录，没有把 `ros2_learning_notes.md` 作为每节课的必改成果物检查。

Fix:

- 已补齐 `ros2_learning_notes.md` 中第 3 周第 1/2/3 小课学习笔记，并在 `CODEX_CONTEXT.md` 记录后续每课结束必须同步更新正文学习笔记。

Prevention note:

- 每节课提交前检查三类文档：课程讲义 `WEEK_*.md`、总学习笔记 `ros2_learning_notes.md`、入口说明 `README.md`。

## 2026-06-12

Symptom:

- 安装 `ros-jazzy-xacro` 后运行 `xacro --version`，命令返回 `xacro: error: no such option: --version`。

Root cause:

- 当前 ROS 2 Jazzy 环境中的 `xacro` 命令不提供 `--version` 选项；这不是安装失败。

Fix:

- 用 `source /opt/ros/jazzy/setup.bash && ros2 pkg prefix xacro` 验证包是否可发现；实际处理文件时用 `xacro <input-file>` 或 `xacro <input-file> -o <output-file>`。

Prevention note:

- 后续检查 Xacro 环境时不要依赖 `xacro --version`；优先检查 `ros2 pkg prefix xacro` 和一次最小 Xacro 展开命令。

## 2026-06-12

Symptom:

- RViz2 中 `RobotModel` 显示 `Status: Ok`，但画面一开始只有 Grid，看不到模型；展开 `TF -> Frames` 也可能暂时为空。

Root cause:

- `RobotModel` 订阅 `/robot_description` 的 QoS 如果是 `Volatile`，RViz 可能错过 `robot_state_publisher` 的 transient local 机器人描述；另外 RViz 刚启动时模型/TF 也可能有短暂刷新延迟。

Fix:

- 将 `src/robot_description/rviz/display.rviz` 中 `Description Topic` 的 `Durability Policy` 设为 `Transient Local`；重新 `colcon build --packages-select robot_description` 并重启 launch。

Prevention note:

- 后续保存 RViz 配置时，检查 `RobotModel -> Description Topic -> Durability Policy` 是否仍为 `Transient Local`。如果 RViz 仍短暂空白，先等 2-5 秒或切换 `RobotModel`/`TF` 勾选状态，再查 `/robot_description` 和 `/tf_static`。

## 2026-06-11

Symptom:

- 第 3 周第 2 小课最初计划用 `joint_state_publisher_gui` 模拟轮子 joint，但 `ros2 pkg prefix joint_state_publisher_gui` 和 `ros2 pkg prefix joint_state_publisher` 都返回 `Package not found`。

Root cause:

- 当前 ROS 2 Jazzy 环境安装了 `robot_state_publisher` 和 `rviz2`，但没有安装 `joint_state_publisher` 系列包；如果 launch 直接启动 GUI，会在运行时缺包失败。

Fix:

- 本课将 `robot_description` 收敛为固定 frame 模型：轮子、摄像头和雷达 joint 均使用 `fixed`，launch 只启动 `robot_state_publisher` 和 RViz2。

Prevention note:

- 后续需要可动 joint 或 GUI 滑条时，先确认 `joint_state_publisher` 是否已安装；未安装前不要把它写成必需运行依赖。

## 2026-06-10

Symptom:

- 运行 `source /opt/ros/jazzy/setup.bash && PYTHONPATH=src/tf2_frame_demo python3 -m unittest ...` 时，测试导入节点模块报 `ModuleNotFoundError: No module named 'rclpy'`。

Root cause:

- 命令里的 `PYTHONPATH=src/tf2_frame_demo` 覆盖了 ROS 2 环境脚本设置的 `/opt/ros/jazzy/lib/python3.12/site-packages`，导致 Python 找不到 `rclpy`。

Fix:

- 追加而不是覆盖：`PYTHONPATH=src/tf2_frame_demo:$PYTHONPATH python3 -m unittest ...`。

Prevention note:

- 需要同时导入本地源码和 ROS 2 Python 包时，先 `source /opt/ros/jazzy/setup.bash`，再把本地路径加到现有 `PYTHONPATH` 前面。

## 2026-06-10

Symptom:

- 在受限沙箱内短时运行 `ros2 launch tf2_frame_demo tf2_demo.launch.py` 时，日志出现大量 `getifaddrs: Operation not permitted` 和 Fast DDS `Error creating socket: Operation not permitted`。

Root cause:

- 沙箱限制网络接口枚举和 UDP socket 创建；这不是 tf2 示例代码或 launch 文件错误。

Fix:

- 对代码正确性优先使用单元测试、`compileall`、`colcon build`、`ros2 launch --show-args` 验证；短时实际启动时只要 listener 能打印 TF 查询结果，可认为示例链路在当前限制下已经跑通。

Prevention note:

- 后续在沙箱内验证 ROS 2 graph/runtime 时，看到 DDS socket 权限噪声不要立即误判代码错误；正常用户终端环境下通常不会出现该限制。

## 2026-06-09

Symptom:

- `ros2 launch turtlesim_p_controller turtlesim_goal.launch.py --show-args` 报 `OSError: [Errno 30] Read-only file system: '/home/sheepyjb/.ros/log/...'`，随后被包装成 `InvalidLaunchFileError`。

Root cause:

- 受限沙箱不能写默认 ROS 日志目录 `/home/sheepyjb/.ros/log`；launch 文件本身没有语法错误。

Fix:

- 在验证命令前设置可写日志目录，例如 `export ROS_LOG_DIR=/tmp/ros2_launch_logs`。

Prevention note:

- 沙箱内验证 `ros2 launch` 时，优先使用 `mkdir -p /tmp/ros2_launch_logs && export ROS_LOG_DIR=/tmp/ros2_launch_logs`，避免把日志目录错误误判为 launch 文件错误。

## 2026-06-08

Symptom:

- `/home/sheepyjb/ros` 初始目录为空但属主是 `root:root`，普通写入失败。

Root cause:

- 目录权限不属于当前用户；同时受限沙箱会预创建只读 `.git/.agents/.codex` 占位目录，容易误判真实仓库状态。

Fix:

- 因目录为空，先删除空目录，再由当前用户重建目录。
- 在非沙箱环境执行 `git init /home/sheepyjb/ros`，然后改默认分支为 `main`。

Prevention note:

- 新会话如果遇到 `bwrap: Can't mkdir /home/sheepyjb/ros/.git: Permission denied` 或 `fatal: not a git repository`，先用非沙箱 `ls -la /home/sheepyjb/ros` 核对真实目录，再判断是否需要重建或初始化仓库。
