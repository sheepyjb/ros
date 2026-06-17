import unittest
from unittest.mock import patch

from nav_msgs.msg import Odometry

from robot_simulation import odom_to_tf
from robot_simulation.odom_to_tf import odometry_to_transform


class FakeNode:
    def __init__(self, raise_on_destroy=False):
        self.destroyed = False
        self.raise_on_destroy = raise_on_destroy

    def destroy_node(self):
        if self.raise_on_destroy:
            raise KeyboardInterrupt
        self.destroyed = True


class FakeRclpy:
    def __init__(self, context_ok):
        self.context_ok = context_ok
        self.shutdown_called = False

    def init(self, args=None):
        pass

    def spin(self, node):
        raise KeyboardInterrupt

    def ok(self):
        return self.context_ok

    def shutdown(self):
        if not self.context_ok:
            raise AssertionError("shutdown should not be called after context shutdown")
        self.shutdown_called = True


class OdometryToTransformTest(unittest.TestCase):
    def test_odometry_pose_becomes_transform(self):
        odometry = Odometry()
        odometry.header.stamp.sec = 12
        odometry.header.stamp.nanosec = 34
        odometry.header.frame_id = "odom"
        odometry.child_frame_id = "base_link"
        odometry.pose.pose.position.x = 1.2
        odometry.pose.pose.position.y = -0.3
        odometry.pose.pose.position.z = 0.0
        odometry.pose.pose.orientation.x = 0.0
        odometry.pose.pose.orientation.y = 0.0
        odometry.pose.pose.orientation.z = 0.25
        odometry.pose.pose.orientation.w = 0.97

        transform = odometry_to_transform(odometry)

        self.assertEqual(odometry.header.stamp, transform.header.stamp)
        self.assertEqual("odom", transform.header.frame_id)
        self.assertEqual("base_link", transform.child_frame_id)
        self.assertAlmostEqual(1.2, transform.transform.translation.x)
        self.assertAlmostEqual(-0.3, transform.transform.translation.y)
        self.assertAlmostEqual(0.0, transform.transform.translation.z)
        self.assertAlmostEqual(0.0, transform.transform.rotation.x)
        self.assertAlmostEqual(0.0, transform.transform.rotation.y)
        self.assertAlmostEqual(0.25, transform.transform.rotation.z)
        self.assertAlmostEqual(0.97, transform.transform.rotation.w)


class OdomToTfShutdownTest(unittest.TestCase):
    def test_main_skips_duplicate_shutdown(self):
        fake_rclpy = FakeRclpy(context_ok=False)
        fake_node = FakeNode()

        with patch.object(odom_to_tf, "rclpy", fake_rclpy), patch.object(
            odom_to_tf,
            "OdomToTf",
            return_value=fake_node,
        ):
            odom_to_tf.main()

        self.assertTrue(fake_node.destroyed)
        self.assertFalse(fake_rclpy.shutdown_called)

    def test_main_ignores_keyboard_interrupt_during_destroy(self):
        fake_rclpy = FakeRclpy(context_ok=False)
        fake_node = FakeNode(raise_on_destroy=True)

        with patch.object(odom_to_tf, "rclpy", fake_rclpy), patch.object(
            odom_to_tf,
            "OdomToTf",
            return_value=fake_node,
        ):
            odom_to_tf.main()

        self.assertFalse(fake_rclpy.shutdown_called)


if __name__ == "__main__":
    unittest.main()
