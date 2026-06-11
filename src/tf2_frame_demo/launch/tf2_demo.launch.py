from launch import LaunchDescription  # launch 文件最终要返回 LaunchDescription。
from launch_ros.actions import Node  # Node 动作用来启动一个 ROS 2 节点进程。


def generate_launch_description():
    """描述本课要一次启动的 4 个节点。"""

    return LaunchDescription(
        [
            Node(
                package="tf2_ros",  # 使用系统自带的 tf2_ros 包。
                executable="static_transform_publisher",  # 发布静态 TF 的命令行节点。
                name="map_to_odom_publisher",  # 给这个进程起一个可读节点名。
                arguments=[
                    "--x",
                    "0.0",  # odom 相对 map 的 x 偏移，本课设为 0。
                    "--y",
                    "0.0",  # odom 相对 map 的 y 偏移，本课设为 0。
                    "--z",
                    "0.0",  # odom 相对 map 的 z 偏移，本课设为 0。
                    "--roll",
                    "0.0",  # odom 相对 map 的 roll 旋转，本课设为 0。
                    "--pitch",
                    "0.0",  # odom 相对 map 的 pitch 旋转，本课设为 0。
                    "--yaw",
                    "0.0",  # odom 相对 map 的 yaw 旋转，本课设为 0。
                    "--frame-id",
                    "map",  # 父坐标系：全局地图坐标系。
                    "--child-frame-id",
                    "odom",  # 子坐标系：里程计坐标系。
                ],
            ),
            Node(
                package="tf2_ros",  # 仍然使用系统自带的 tf2_ros 包。
                executable="static_transform_publisher",  # 摄像头安装位姿是静态 TF。
                name="base_to_camera_publisher",  # 节点名表示它发布 base_link -> camera_link。
                arguments=[
                    "--x",
                    "0.25",  # camera_link 在 base_link 前方 0.25 米。
                    "--y",
                    "0.0",  # camera_link 不向左/右偏移。
                    "--z",
                    "0.20",  # camera_link 在 base_link 上方 0.20 米。
                    "--roll",
                    "0.0",  # 摄像头相对底盘没有 roll 旋转。
                    "--pitch",
                    "0.0",  # 摄像头相对底盘没有 pitch 旋转。
                    "--yaw",
                    "0.0",  # 摄像头相对底盘没有 yaw 旋转。
                    "--frame-id",
                    "base_link",  # 父坐标系：机器人底盘坐标系。
                    "--child-frame-id",
                    "camera_link",  # 子坐标系：摄像头坐标系。
                ],
            ),
            Node(
                package="tf2_frame_demo",  # 本课自定义示例包。
                executable="dynamic_frame_broadcaster",  # 发布 odom -> base_link 动态 TF。
                name="dynamic_frame_broadcaster",  # 节点名。
                output="screen",  # 把节点日志输出到当前终端。
            ),
            Node(
                package="tf2_frame_demo",  # 本课自定义示例包。
                executable="frame_listener",  # 查询 map -> camera_link 并打印。
                name="frame_listener",  # 节点名。
                output="screen",  # 把查询结果输出到当前终端。
            ),
        ]
    )
