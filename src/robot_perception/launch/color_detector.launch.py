from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    perception_share = Path(get_package_share_directory("robot_perception"))
    config_path = perception_share / "config" / "color_detector.yaml"

    use_sim_time = LaunchConfiguration("use_sim_time")
    target_color = LaunchConfiguration("target_color")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
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
                    str(config_path),
                    {"use_sim_time": use_sim_time},
                    {"target_color": target_color},
                ],
            ),
        ]
    )
