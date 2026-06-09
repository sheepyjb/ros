import rclpy  # ROS 2 Python 客户端库，写 Python 节点必须用它。
from geometry_msgs.msg import Twist  # Twist 是速度消息，用来控制乌龟运动。
from rclpy.node import Node  # Node 是 ROS 2 Python 节点的基类。
from turtlesim.msg import Pose  # Pose 是 turtlesim 发布的乌龟位姿消息。

from turtlesim_p_controller.controller_math import (
    ControllerConfig,  # 控制参数数据类。
    TurtlePose,  # 乌龟位姿数据类。
    compute_velocity_command,  # 根据位姿和参数计算速度命令。
)


class TurtleGoalController(Node):
    """订阅乌龟位姿并发布速度命令的 ROS 2 节点。"""

    def __init__(self):
        super().__init__("turtle_goal_controller")  # 初始化节点，并设置节点名。
        self.declare_parameter("goal_x", 8.0)  # 目标点 x 坐标，默认 8.0。
        self.declare_parameter("goal_y", 8.0)  # 目标点 y 坐标，默认 8.0。
        self.declare_parameter("linear_gain", 1.2)  # 线速度 P 控制比例系数。
        self.declare_parameter("angular_gain", 4.0)  # 角速度 P 控制比例系数。
        self.declare_parameter("max_linear_speed", 2.0)  # 最大线速度。
        self.declare_parameter("max_angular_speed", 4.0)  # 最大角速度。
        self.declare_parameter("goal_tolerance", 0.15)  # 到目标点多近算到达。

        self._cmd_vel_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.create_subscription(Pose, "/turtle1/pose", self._on_pose, 10)

    def _on_pose(self, msg: Pose) -> None:
        """每收到一次 /turtle1/pose，就计算并发布一次速度命令。"""

        config = self._read_config()  # 读取当前 ROS 2 参数。
        pose = TurtlePose(x=msg.x, y=msg.y, theta=msg.theta)  # 转成自己的位姿数据类。
        command = compute_velocity_command(pose, config)  # 调用纯数学控制算法。

        twist = Twist()  # 创建 ROS 2 速度消息。
        twist.linear.x = command.linear_x  # 填入前进速度。
        twist.angular.z = command.angular_z  # 填入转向速度。
        self._cmd_vel_pub.publish(twist)  # 发布到 /turtle1/cmd_vel。

    def _read_config(self) -> ControllerConfig:
        """从 ROS 2 参数系统读取当前控制器配置。"""

        return ControllerConfig(
            goal_x=self.get_parameter("goal_x").value,  # 读取目标 x。
            goal_y=self.get_parameter("goal_y").value,  # 读取目标 y。
            linear_gain=self.get_parameter("linear_gain").value,  # 读取线速度系数。
            angular_gain=self.get_parameter("angular_gain").value,  # 读取角速度系数。
            max_linear_speed=self.get_parameter("max_linear_speed").value,
            max_angular_speed=self.get_parameter("max_angular_speed").value,
            goal_tolerance=self.get_parameter("goal_tolerance").value,
        )


def main(args=None):
    rclpy.init(args=args)  # 初始化 ROS 2 Python 运行环境。
    node = TurtleGoalController()  # 创建自己的控制器节点。
    try:
        rclpy.spin(node)  # 让节点持续运行，等待 topic 消息触发回调。
    finally:
        node.destroy_node()  # 退出前销毁节点，释放资源。
        rclpy.shutdown()  # 关闭 ROS 2 Python 运行环境。


if __name__ == "__main__":
    main()  # 允许直接用 python 运行这个文件。
