# CODEX_PITFALLS

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
