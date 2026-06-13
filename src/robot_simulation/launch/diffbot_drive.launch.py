from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    simulation_share = Path(get_package_share_directory("robot_simulation"))
    ros_gz_sim_share = Path(get_package_share_directory("ros_gz_sim"))

    world_path = simulation_share / "worlds" / "diffbot_drive.world.sdf"
    bridge_config_path = simulation_share / "config" / "diff_drive_bridge.yaml"
    gz_launch_path = ros_gz_sim_share / "launch" / "gz_sim.launch.py"

    return LaunchDescription(
        [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(str(gz_launch_path)),
                launch_arguments={
                    "gz_args": f"-r {world_path}",
                    "on_exit_shutdown": "True",
                }.items(),
            ),
            Node(
                package="ros_gz_bridge",
                executable="parameter_bridge",
                name="diff_drive_bridge",
                output="screen",
                parameters=[{"config_file": str(bridge_config_path)}],
            ),
        ]
    )
