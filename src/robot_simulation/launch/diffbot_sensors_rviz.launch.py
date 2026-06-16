from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    simulation_share = Path(get_package_share_directory("robot_simulation"))
    description_share = Path(get_package_share_directory("robot_description"))
    ros_gz_sim_share = Path(get_package_share_directory("ros_gz_sim"))

    world_path = simulation_share / "worlds" / "diffbot_sensors.world.sdf"
    bridge_config_path = simulation_share / "config" / "sensor_bridge.yaml"
    rviz_path = simulation_share / "rviz" / "sensors.rviz"
    gz_launch_path = ros_gz_sim_share / "launch" / "gz_sim.launch.py"
    xacro_path = description_share / "urdf" / "diffbot.urdf.xacro"

    robot_description = xacro.process_file(str(xacro_path)).toxml()

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
                name="sensor_bridge",
                output="screen",
                parameters=[{"config_file": str(bridge_config_path)}],
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[
                    {"use_sim_time": True},
                    {"robot_description": robot_description},
                ],
            ),
            Node(
                package="robot_simulation",
                executable="odom_to_tf",
                name="odom_to_tf",
                output="screen",
                parameters=[{"use_sim_time": True}],
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                arguments=["-d", str(rviz_path)],
                parameters=[{"use_sim_time": True}],
            ),
        ]
    )
