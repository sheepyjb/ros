from pathlib import Path  # 用 pathlib 拼路径，比手写字符串路径更清楚。

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # get_package_share_directory 找的是 install/ 下的 share 目录。
    # 所以每次改 launch/config 后都要重新 colcon build，安装态才会更新。
    perception_share = Path(get_package_share_directory("robot_perception"))
    config_path = perception_share / "config" / "color_detector.yaml"

    # LaunchConfiguration 代表运行 ros2 launch 时传进来的参数。
    # 例如 target_color:=green 会覆盖默认 red。
    use_sim_time = LaunchConfiguration("use_sim_time")
    target_color = LaunchConfiguration("target_color")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
                # Gazebo 仿真里建议使用 /clock，否则 ROS 节点时间和仿真时间会不一致。
                description="Use Gazebo simulation time.",
            ),
            DeclareLaunchArgument(
                "target_color",
                default_value="red",
                description="Color target to detect: red or green.",
            ),
            Node(
                package="robot_perception",
                executable="image_detector_node",
                name="image_detector_node",
                output="screen",
                parameters=[
                    str(config_path),  # 先加载 YAML 中的默认参数。
                    {"use_sim_time": use_sim_time},  # 再允许 launch 参数覆盖 use_sim_time。
                    {"target_color": target_color},  # 允许命令行快速切换 red/green。
                ],
            ),
        ]
    )
