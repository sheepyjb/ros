import unittest
from unittest.mock import patch

from robot_perception import image_detector_node


class FakeNode:
    """替代真实 ROS 2 Node，专门测试 main() 的清理逻辑。"""

    def __init__(self, raise_on_destroy=False):
        self.destroyed = False
        self.raise_on_destroy = raise_on_destroy

    def destroy_node(self):
        # 模拟真实 launch 退出时，destroy_node() 过程中也可能再次收到 Ctrl-C。
        if self.raise_on_destroy:
            raise KeyboardInterrupt
        self.destroyed = True


class FakeRclpy:
    """替代 rclpy，避免单元测试真的启动 ROS 2 graph。"""

    def __init__(self, context_ok):
        self.context_ok = context_ok
        self.shutdown_called = False

    def init(self, args=None):
        pass

    def spin(self, node):
        # 模拟用户 Ctrl-C，让 main() 走到 finally 清理分支。
        raise KeyboardInterrupt

    def ok(self):
        return self.context_ok

    def shutdown(self):
        # 如果 context 已经关闭，main() 不应再次调用 shutdown()。
        if not self.context_ok:
            raise AssertionError("shutdown should not be called after context shutdown")
        self.shutdown_called = True


class ImageDetectorShutdownTest(unittest.TestCase):
    """Ctrl-C 后 image_detector_node 应和已有 ROS 节点一样干净退出。"""

    def test_main_skips_duplicate_shutdown(self):
        fake_rclpy = FakeRclpy(context_ok=False)
        fake_node = FakeNode()

        # patch 掉真实 rclpy 和 ImageDetectorNode，只测试 main() 的退出控制流。
        with patch.object(image_detector_node, "rclpy", fake_rclpy), patch.object(
            image_detector_node,
            "ImageDetectorNode",
            return_value=fake_node,
        ):
            image_detector_node.main()

        self.assertTrue(fake_node.destroyed)
        self.assertFalse(fake_rclpy.shutdown_called)

    def test_main_ignores_keyboard_interrupt_during_destroy(self):
        fake_rclpy = FakeRclpy(context_ok=False)
        fake_node = FakeNode(raise_on_destroy=True)

        # 这个测试锁定之前发现的坑：destroy_node() 中再次 KeyboardInterrupt 不应打印 traceback。
        with patch.object(image_detector_node, "rclpy", fake_rclpy), patch.object(
            image_detector_node,
            "ImageDetectorNode",
            return_value=fake_node,
        ):
            image_detector_node.main()

        self.assertFalse(fake_rclpy.shutdown_called)


if __name__ == "__main__":
    unittest.main()
