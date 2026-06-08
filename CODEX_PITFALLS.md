# CODEX_PITFALLS

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
