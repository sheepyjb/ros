import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    controller_share = get_package_share_directory("turtlesim_p_controller")
    controller_params = os.path.join(controller_share, "config", "goal_controller.yaml")

    return LaunchDescription(
        [
            Node(
                package="turtlesim",
                executable="turtlesim_node",
                name="turtlesim",
                output="screen",
            ),
            Node(
                package="turtlesim_p_controller",
                executable="turtle_goal_controller",
                name="turtle_goal_controller",
                parameters=[controller_params],
                output="screen",
            ),
        ]
    )
