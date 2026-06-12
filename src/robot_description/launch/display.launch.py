from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_share = Path(get_package_share_directory("robot_description"))
    urdf_path = package_share / "urdf" / "diffbot.urdf"
    rviz_path = package_share / "rviz" / "display.rviz"

    robot_description = urdf_path.read_text(encoding="utf-8")

    return LaunchDescription(
        [
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[{"robot_description": robot_description}],
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                arguments=["-d", str(rviz_path)],
            ),
        ]
    )
