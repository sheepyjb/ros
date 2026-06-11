import math
import unittest

from tf2_frame_demo.frame_math import circular_pose
from tf2_frame_demo.frame_math import quaternion_to_yaw
from tf2_frame_demo.frame_math import yaw_to_quaternion


class FrameMathTest(unittest.TestCase):
    """检查不依赖 ROS 2 runtime 的坐标数学。"""

    def test_yaw_to_quaternion_round_trip(self):
        yaw = math.pi / 2.0
        quaternion = yaw_to_quaternion(yaw)

        self.assertAlmostEqual(quaternion.x, 0.0)
        self.assertAlmostEqual(quaternion.y, 0.0)
        self.assertAlmostEqual(quaternion_to_yaw(quaternion), yaw)

    def test_circular_pose_starts_on_positive_x_axis(self):
        pose = circular_pose(time_seconds=0.0, radius=2.0, angular_speed=0.5)

        self.assertAlmostEqual(pose.x, 2.0)
        self.assertAlmostEqual(pose.y, 0.0)
        self.assertAlmostEqual(pose.yaw, math.pi / 2.0)

    def test_circular_pose_after_quarter_turn(self):
        time_seconds = (math.pi / 2.0) / 0.5
        pose = circular_pose(time_seconds=time_seconds, radius=2.0, angular_speed=0.5)

        self.assertAlmostEqual(pose.x, 0.0, places=6)
        self.assertAlmostEqual(pose.y, 2.0, places=6)
        self.assertAlmostEqual(pose.yaw, math.pi, places=6)


if __name__ == "__main__":
    unittest.main()
