import unittest
from unittest.mock import patch

from robot_perception import image_detector_node


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


class ImageDetectorShutdownTest(unittest.TestCase):
    """Ctrl-C 后 image_detector_node 应和已有 ROS 节点一样干净退出。"""

    def test_main_skips_duplicate_shutdown(self):
        fake_rclpy = FakeRclpy(context_ok=False)
        fake_node = FakeNode()

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

        with patch.object(image_detector_node, "rclpy", fake_rclpy), patch.object(
            image_detector_node,
            "ImageDetectorNode",
            return_value=fake_node,
        ):
            image_detector_node.main()

        self.assertFalse(fake_rclpy.shutdown_called)


if __name__ == "__main__":
    unittest.main()
