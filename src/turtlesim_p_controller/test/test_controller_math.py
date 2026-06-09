import math  # 测试角度归一化时要用 pi。
import unittest  # Python 标准库测试框架。

from turtlesim_p_controller.controller_math import (
    ControllerConfig,  # 控制参数数据类。
    TurtlePose,  # 乌龟位姿数据类。
    compute_velocity_command,  # 要测试的核心控制函数。
    normalize_angle,  # 要测试的角度归一化函数。
)


class ControllerMathTest(unittest.TestCase):
    """测试纯数学控制逻辑，不依赖 ROS 2 图形窗口。"""

    def test_normalize_angle_wraps_to_pi_range(self):
        self.assertAlmostEqual(normalize_angle(3 * math.pi), math.pi)  # 3pi 等价于 pi。
        self.assertAlmostEqual(normalize_angle(-3 * math.pi), -math.pi)  # -3pi 等价于 -pi。
        self.assertAlmostEqual(normalize_angle(0.5), 0.5)  # 已在范围内的角度不变。

    def test_compute_velocity_command_moves_toward_goal(self):
        # 目标在正前方，所以应该前进，不需要转向。
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

        command = compute_velocity_command(pose, config)  # 调用被测试的控制函数。

        self.assertGreater(command.linear_x, 0.0)  # 应该向前走。
        self.assertAlmostEqual(command.angular_z, 0.0)  # 正前方目标不需要转。
        self.assertLessEqual(command.linear_x, config.max_linear_speed)  # 不能超过限速。

    def test_compute_velocity_command_turns_shortest_direction(self):
        # 目标在左上方，所以应该产生正角速度，让乌龟左转。
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

        command = compute_velocity_command(pose, config)  # 计算速度命令。

        self.assertGreater(command.angular_z, 0.0)  # 正角速度表示向左转。
        self.assertLessEqual(abs(command.angular_z), config.max_angular_speed)  # 不超过角速度上限。

    def test_compute_velocity_command_stops_inside_tolerance(self):
        # 目标点离当前位置很近，应该认为已经到达并停止。
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

        command = compute_velocity_command(pose, config)  # 计算速度命令。

        self.assertEqual(command.linear_x, 0.0)  # 到达后不前进。
        self.assertEqual(command.angular_z, 0.0)  # 到达后不转向。


if __name__ == "__main__":
    unittest.main()  # 允许直接运行本文件执行测试。
