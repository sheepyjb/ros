import unittest
from unittest.mock import patch

from tf2_frame_demo import dynamic_frame_broadcaster
from tf2_frame_demo import frame_listener


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


class NodeShutdownTest(unittest.TestCase):
    """Ctrl-C 后 rclpy context 已关闭时，节点应干净退出。"""

    def assert_main_skips_duplicate_shutdown(self, module, node_class_name):
        fake_rclpy = FakeRclpy(context_ok=False)
        fake_node = FakeNode()

        with patch.object(module, "rclpy", fake_rclpy), patch.object(
            module, node_class_name, return_value=fake_node
        ):
            module.main()

        self.assertTrue(fake_node.destroyed)
        self.assertFalse(fake_rclpy.shutdown_called)

    def test_dynamic_frame_broadcaster_skips_duplicate_shutdown(self):
        self.assert_main_skips_duplicate_shutdown(
            dynamic_frame_broadcaster,
            "DynamicFrameBroadcaster",
        )

    def test_frame_listener_skips_duplicate_shutdown(self):
        self.assert_main_skips_duplicate_shutdown(
            frame_listener,
            "FrameListener",
        )

    def assert_main_ignores_keyboard_interrupt_during_destroy(
        self,
        module,
        node_class_name,
    ):
        fake_rclpy = FakeRclpy(context_ok=False)
        fake_node = FakeNode(raise_on_destroy=True)

        with patch.object(module, "rclpy", fake_rclpy), patch.object(
            module, node_class_name, return_value=fake_node
        ):
            module.main()

        self.assertFalse(fake_rclpy.shutdown_called)

    def test_dynamic_frame_broadcaster_ignores_interrupt_during_destroy(self):
        self.assert_main_ignores_keyboard_interrupt_during_destroy(
            dynamic_frame_broadcaster,
            "DynamicFrameBroadcaster",
        )

    def test_frame_listener_ignores_interrupt_during_destroy(self):
        self.assert_main_ignores_keyboard_interrupt_during_destroy(
            frame_listener,
            "FrameListener",
        )


if __name__ == "__main__":
    unittest.main()
