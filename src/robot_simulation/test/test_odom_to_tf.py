import unittest

from nav_msgs.msg import Odometry

from robot_simulation.odom_to_tf import odometry_to_transform


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


if __name__ == "__main__":
    unittest.main()
