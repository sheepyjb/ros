import ast
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


class BringupAssetsTest(unittest.TestCase):
    """检查 robot_bringup 是否只承担启动编排包的最小职责。"""

    def test_package_files_exist(self):
        self.assertTrue((PACKAGE_ROOT / "package.xml").is_file())
        self.assertTrue((PACKAGE_ROOT / "setup.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "resource" / "robot_bringup").is_file())
        self.assertTrue((PACKAGE_ROOT / "launch" / "turtlesim_goal.launch.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "launch" / "display_robot.launch.py").is_file())

    def test_setup_installs_launch_files(self):
        setup_path = PACKAGE_ROOT / "setup.py"
        if not setup_path.is_file():
            self.fail("robot_bringup/setup.py should exist")

        setup_tree = ast.parse(setup_path.read_text(encoding="utf-8"))
        string_literals = {
            node.value
            for node in ast.walk(setup_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }

        self.assertIn("launch/*.launch.py", string_literals)

    def test_package_declares_bringup_dependencies(self):
        package_path = PACKAGE_ROOT / "package.xml"
        if not package_path.is_file():
            self.fail("robot_bringup/package.xml should exist")

        package_xml = ET.parse(package_path)
        dependencies = {
            element.text
            for element in package_xml.findall(".//depend")
        } | {
            element.text
            for element in package_xml.findall(".//exec_depend")
        }

        self.assertIn("turtlesim", dependencies)
        self.assertIn("turtlesim_p_controller", dependencies)
        self.assertIn("robot_description", dependencies)
        self.assertIn("launch_ros", dependencies)

    def test_display_robot_launch_includes_robot_description_display(self):
        launch_path = PACKAGE_ROOT / "launch" / "display_robot.launch.py"
        if not launch_path.is_file():
            self.fail("robot_bringup/launch/display_robot.launch.py should exist")

        launch_tree = ast.parse(launch_path.read_text(encoding="utf-8"))
        string_literals = {
            node.value
            for node in ast.walk(launch_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }

        self.assertIn("robot_description", string_literals)
        self.assertIn("display.launch.py", string_literals)
        self.assertIn("IncludeLaunchDescription", launch_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
