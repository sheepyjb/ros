import rclpy
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from tf2_ros import TransformBroadcaster


def odometry_to_transform(odometry):
    transform = TransformStamped()
    transform.header.stamp = odometry.header.stamp
    transform.header.frame_id = odometry.header.frame_id
    transform.child_frame_id = odometry.child_frame_id
    transform.transform.translation.x = odometry.pose.pose.position.x
    transform.transform.translation.y = odometry.pose.pose.position.y
    transform.transform.translation.z = odometry.pose.pose.position.z
    transform.transform.rotation = odometry.pose.pose.orientation
    return transform


class OdomToTf(Node):
    def __init__(self):
        super().__init__("odom_to_tf")
        self._broadcaster = TransformBroadcaster(self)
        self.create_subscription(Odometry, "/odom", self._handle_odometry, 10)

    def _handle_odometry(self, odometry):
        if not odometry.header.frame_id or not odometry.child_frame_id:
            self.get_logger().warn("Ignore odometry without frame_id or child_frame_id")
            return

        self._broadcaster.sendTransform(odometry_to_transform(odometry))


def main(args=None):
    rclpy.init(args=args)
    node = OdomToTf()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
