from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    robot_description_share = Path(get_package_share_directory("robot_description"))
    display_launch = robot_description_share / "launch" / "display.launch.py"

    return LaunchDescription(
        [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(str(display_launch)),
            ),
        ]
    )
