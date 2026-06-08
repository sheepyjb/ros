import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from turtlesim.msg import Pose

from turtlesim_p_controller.controller_math import (
    ControllerConfig,
    TurtlePose,
    compute_velocity_command,
)


class TurtleGoalController(Node):
    def __init__(self):
        super().__init__("turtle_goal_controller")
        self.declare_parameter("goal_x", 8.0)
        self.declare_parameter("goal_y", 8.0)
        self.declare_parameter("linear_gain", 1.2)
        self.declare_parameter("angular_gain", 4.0)
        self.declare_parameter("max_linear_speed", 2.0)
        self.declare_parameter("max_angular_speed", 4.0)
        self.declare_parameter("goal_tolerance", 0.15)

        self._cmd_vel_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.create_subscription(Pose, "/turtle1/pose", self._on_pose, 10)

    def _on_pose(self, msg: Pose) -> None:
        config = self._read_config()
        pose = TurtlePose(x=msg.x, y=msg.y, theta=msg.theta)
        command = compute_velocity_command(pose, config)

        twist = Twist()
        twist.linear.x = command.linear_x
        twist.angular.z = command.angular_z
        self._cmd_vel_pub.publish(twist)

    def _read_config(self) -> ControllerConfig:
        return ControllerConfig(
            goal_x=self.get_parameter("goal_x").value,
            goal_y=self.get_parameter("goal_y").value,
            linear_gain=self.get_parameter("linear_gain").value,
            angular_gain=self.get_parameter("angular_gain").value,
            max_linear_speed=self.get_parameter("max_linear_speed").value,
            max_angular_speed=self.get_parameter("max_angular_speed").value,
            goal_tolerance=self.get_parameter("goal_tolerance").value,
        )


def main(args=None):
    rclpy.init(args=args)
    node = TurtleGoalController()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
