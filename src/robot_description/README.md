# robot_description

第 3 周第 2/3 小课使用的机器人模型包。

这个包只保存机器人描述资产：

```text
urdf/diffbot.urdf
urdf/diffbot.urdf.xacro
urdf/diffbot_materials.xacro
urdf/diffbot_components.xacro
launch/display.launch.py
rviz/display.rviz
```

运行：

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select robot_description
source install/setup.bash
ros2 launch robot_description display.launch.py
```

第 3 周第 3 小课推荐从 `robot_bringup` 统一入口启动：

```bash
ros2 launch robot_bringup display_robot.launch.py
```
