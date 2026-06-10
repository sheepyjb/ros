import math
import unittest

from turtlesim_p_controller.goal_service import validate_goal_coordinates


class GoalServiceTest(unittest.TestCase):
    """测试设置目标点服务复用的纯 Python 校验逻辑。"""

    def test_accepts_finite_goal_coordinates(self):
        is_valid, message = validate_goal_coordinates(2.0, 8.0)

        self.assertTrue(is_valid)
        self.assertEqual(message, "目标点已更新为 (2.00, 8.00)。")

    def test_rejects_non_finite_goal_coordinates(self):
        for x, y in [
            (math.nan, 8.0),
            (2.0, math.nan),
            (math.inf, 8.0),
            (2.0, -math.inf),
        ]:
            with self.subTest(x=x, y=y):
                is_valid, message = validate_goal_coordinates(x, y)

                self.assertFalse(is_valid)
                self.assertEqual(message, "目标坐标必须是有限数字。")


if __name__ == "__main__":
    unittest.main()
