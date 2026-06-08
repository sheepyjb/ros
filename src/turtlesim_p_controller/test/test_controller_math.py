import math
import unittest

from turtlesim_p_controller.controller_math import (
    ControllerConfig,
    TurtlePose,
    compute_velocity_command,
    normalize_angle,
)


class ControllerMathTest(unittest.TestCase):
    def test_normalize_angle_wraps_to_pi_range(self):
        self.assertAlmostEqual(normalize_angle(3 * math.pi), math.pi)
        self.assertAlmostEqual(normalize_angle(-3 * math.pi), -math.pi)
        self.assertAlmostEqual(normalize_angle(0.5), 0.5)

    def test_compute_velocity_command_moves_toward_goal(self):
        config = ControllerConfig(
            goal_x=8.0,
            goal_y=5.5,
            linear_gain=1.0,
            angular_gain=2.0,
            max_linear_speed=2.0,
            max_angular_speed=3.0,
            goal_tolerance=0.15,
        )
        pose = TurtlePose(x=5.5, y=5.5, theta=0.0)

        command = compute_velocity_command(pose, config)

        self.assertGreater(command.linear_x, 0.0)
        self.assertAlmostEqual(command.angular_z, 0.0)
        self.assertLessEqual(command.linear_x, config.max_linear_speed)

    def test_compute_velocity_command_turns_shortest_direction(self):
        config = ControllerConfig(
            goal_x=5.5,
            goal_y=8.0,
            linear_gain=1.0,
            angular_gain=2.0,
            max_linear_speed=2.0,
            max_angular_speed=3.0,
            goal_tolerance=0.15,
        )
        pose = TurtlePose(x=5.5, y=5.5, theta=0.0)

        command = compute_velocity_command(pose, config)

        self.assertGreater(command.angular_z, 0.0)
        self.assertLessEqual(abs(command.angular_z), config.max_angular_speed)

    def test_compute_velocity_command_stops_inside_tolerance(self):
        config = ControllerConfig(
            goal_x=5.55,
            goal_y=5.5,
            linear_gain=1.0,
            angular_gain=2.0,
            max_linear_speed=2.0,
            max_angular_speed=3.0,
            goal_tolerance=0.15,
        )
        pose = TurtlePose(x=5.5, y=5.5, theta=0.0)

        command = compute_velocity_command(pose, config)

        self.assertEqual(command.linear_x, 0.0)
        self.assertEqual(command.angular_z, 0.0)


if __name__ == "__main__":
    unittest.main()
