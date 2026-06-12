import ast
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


class RobotDescriptionAssetsTest(unittest.TestCase):
    """检查第 3 周第 2 小课的 robot_description 资产。"""

    def test_package_files_exist(self):
        self.assertTrue((PACKAGE_ROOT / "package.xml").is_file())
        self.assertTrue((PACKAGE_ROOT / "setup.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "setup.cfg").is_file())
        self.assertTrue((PACKAGE_ROOT / "resource" / "robot_description").is_file())
        self.assertTrue((PACKAGE_ROOT / "launch" / "display.launch.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "urdf" / "diffbot.urdf").is_file())
        self.assertTrue((PACKAGE_ROOT / "rviz" / "display.rviz").is_file())
        self.assertTrue((PACKAGE_ROOT / "WEEK_03_02_ROBOT_DESCRIPTION_URDF.md").is_file())

    def test_setup_installs_description_assets(self):
        setup_path = PACKAGE_ROOT / "setup.py"
        if not setup_path.is_file():
            self.fail("robot_description/setup.py should exist")

        setup_tree = ast.parse(setup_path.read_text(encoding="utf-8"))
        string_literals = {
            node.value
            for node in ast.walk(setup_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }

        self.assertIn("launch/*.launch.py", string_literals)
        self.assertIn("urdf/*.urdf", string_literals)
        self.assertIn("rviz/*.rviz", string_literals)

    def test_package_declares_display_dependencies(self):
        package_path = PACKAGE_ROOT / "package.xml"
        if not package_path.is_file():
            self.fail("robot_description/package.xml should exist")

        package_xml = ET.parse(package_path)
        dependencies = {
            element.text
            for element in package_xml.findall(".//depend")
        } | {
            element.text
            for element in package_xml.findall(".//exec_depend")
        }

        self.assertIn("ament_index_python", dependencies)
        self.assertIn("launch_ros", dependencies)
        self.assertNotIn("joint_state_publisher", dependencies)
        self.assertNotIn("joint_state_publisher_gui", dependencies)
        self.assertIn("robot_state_publisher", dependencies)
        self.assertIn("rviz2", dependencies)

    def test_launch_uses_robot_state_publisher_only(self):
        launch_path = PACKAGE_ROOT / "launch" / "display.launch.py"
        if not launch_path.is_file():
            self.fail("robot_description/launch/display.launch.py should exist")

        launch_tree = ast.parse(launch_path.read_text(encoding="utf-8"))
        string_literals = {
            node.value
            for node in ast.walk(launch_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }

        self.assertIn("robot_state_publisher", string_literals)
        self.assertIn("rviz2", string_literals)
        self.assertNotIn("joint_state_publisher", string_literals)
        self.assertNotIn("joint_state_publisher_gui", string_literals)

    def test_rviz_keeps_tf_names_readable(self):
        rviz_path = PACKAGE_ROOT / "rviz" / "display.rviz"
        if not rviz_path.is_file():
            self.fail("robot_description/rviz/display.rviz should exist")

        marker_scale = None
        view_distance = None
        for line in rviz_path.read_text(encoding="utf-8").splitlines():
            stripped_line = line.strip()
            if stripped_line.startswith("Marker Scale:"):
                marker_scale = float(stripped_line.split(":", 1)[1].strip())
            if stripped_line.startswith("Distance:"):
                view_distance = float(stripped_line.split(":", 1)[1].strip())

        self.assertIsNotNone(marker_scale)
        self.assertLessEqual(marker_scale, 0.2)
        self.assertIsNotNone(view_distance)
        self.assertGreaterEqual(view_distance, 1.8)

    def test_rviz_robot_model_uses_transient_local_description_topic(self):
        rviz_path = PACKAGE_ROOT / "rviz" / "display.rviz"
        if not rviz_path.is_file():
            self.fail("robot_description/rviz/display.rviz should exist")

        rviz_config = rviz_path.read_text(encoding="utf-8")

        self.assertIn("Description Source: Topic", rviz_config)
        self.assertIn("Value: /robot_description", rviz_config)
        self.assertIn("Durability Policy: Transient Local", rviz_config)

    def test_urdf_contains_robot_links_and_frames(self):
        urdf_path = PACKAGE_ROOT / "urdf" / "diffbot.urdf"
        if not urdf_path.is_file():
            self.fail("robot_description/urdf/diffbot.urdf should exist")

        urdf_xml = ET.parse(urdf_path)
        robot = urdf_xml.getroot()
        self.assertEqual("robot", robot.tag)
        self.assertEqual("diffbot", robot.attrib["name"])

        links = {link.attrib["name"] for link in robot.findall("link")}
        joints = {joint.attrib["name"]: joint for joint in robot.findall("joint")}

        self.assertIn("base_link", links)
        self.assertIn("left_wheel_link", links)
        self.assertIn("right_wheel_link", links)
        self.assertIn("camera_link", links)
        self.assertIn("camera_optical_frame", links)
        self.assertIn("laser_link", links)

        self.assertEqual("fixed", joints["left_wheel_joint"].attrib["type"])
        self.assertEqual("fixed", joints["right_wheel_joint"].attrib["type"])
        self.assertEqual("fixed", joints["camera_joint"].attrib["type"])
        self.assertEqual("fixed", joints["camera_optical_joint"].attrib["type"])
        self.assertEqual("fixed", joints["laser_joint"].attrib["type"])

        self.assertEqual("base_link", joints["camera_joint"].find("parent").attrib["link"])
        self.assertEqual("camera_link", joints["camera_optical_joint"].find("parent").attrib["link"])
        self.assertEqual("base_link", joints["laser_joint"].find("parent").attrib["link"])


if __name__ == "__main__":
    unittest.main()
