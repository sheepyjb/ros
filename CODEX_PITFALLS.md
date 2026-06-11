# CODEX_PITFALLS

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
