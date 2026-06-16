from pathlib import Path  # 用 pathlib 拼路径，避免手写路径分隔符。

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    perception_share = Path(get_package_share_directory("robot_perception"))
    config_path = perception_share / "config" / "yolo_detector.yaml"

    use_sim_time = LaunchConfiguration("use_sim_time")
    yolo_model_path = LaunchConfiguration("yolo_model_path")
    yolo_confidence_threshold = LaunchConfiguration("yolo_confidence_threshold")
    yolo_target_class = LaunchConfiguration("yolo_target_class")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
                description="Use Gazebo simulation time.",
            ),
            DeclareLaunchArgument(
                "yolo_model_path",
                default_value="yolov8n.pt",
                description="Ultralytics model name or local weights path.",
            ),
            DeclareLaunchArgument(
                "yolo_confidence_threshold",
                default_value="0.25",
                description="Minimum YOLO confidence to accept a detection.",
            ),
            DeclareLaunchArgument(
                "yolo_target_class",
                default_value="",
                description="Class name to keep. Empty string accepts any class.",
            ),
            Node(
                package="robot_perception",
                executable="image_detector_node",
                name="image_detector_node",
                output="screen",
                parameters=[
                    str(config_path),
                    {"use_sim_time": use_sim_time},
                    {"yolo_model_path": yolo_model_path},
                    {"yolo_confidence_threshold": yolo_confidence_threshold},
                    {"yolo_target_class": yolo_target_class},
                ],
            ),
        ]
    )
