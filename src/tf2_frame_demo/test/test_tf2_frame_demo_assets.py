import ast
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


class Tf2FrameDemoAssetsTest(unittest.TestCase):
    """检查 tf2_frame_demo 的 package 结构和安装声明。"""

    def test_package_files_exist(self):
        self.assertTrue((PACKAGE_ROOT / "package.xml").is_file())
        self.assertTrue((PACKAGE_ROOT / "setup.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "setup.cfg").is_file())
        self.assertTrue((PACKAGE_ROOT / "resource" / "tf2_frame_demo").is_file())
        self.assertTrue((PACKAGE_ROOT / "launch" / "tf2_demo.launch.py").is_file())

    def test_setup_declares_console_scripts_and_launch_assets(self):
        setup_tree = ast.parse((PACKAGE_ROOT / "setup.py").read_text(encoding="utf-8"))
        string_literals = {
            node.value
            for node in ast.walk(setup_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }

        self.assertIn("launch/*.launch.py", string_literals)
        self.assertIn(
            "dynamic_frame_broadcaster = tf2_frame_demo.dynamic_frame_broadcaster:main",
            string_literals,
        )
        self.assertIn(
            "frame_listener = tf2_frame_demo.frame_listener:main",
            string_literals,
        )

    def test_package_declares_tf2_dependencies(self):
        package_xml = ET.parse(PACKAGE_ROOT / "package.xml")
        dependencies = {
            element.text
            for element in package_xml.findall(".//depend")
        } | {
            element.text
            for element in package_xml.findall(".//exec_depend")
        }

        self.assertIn("geometry_msgs", dependencies)
        self.assertIn("rclpy", dependencies)
        self.assertIn("tf2_ros", dependencies)
        self.assertIn("tf2_tools", dependencies)
        self.assertIn("launch_ros", dependencies)


if __name__ == "__main__":
    unittest.main()
