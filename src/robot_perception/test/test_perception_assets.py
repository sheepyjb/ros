import ast
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


class RobotPerceptionAssetsTest(unittest.TestCase):
    """检查第 5 周第 1 小课的感知包资产。"""

    def test_package_files_exist(self):
        self.assertTrue((PACKAGE_ROOT / "package.xml").is_file())
        self.assertTrue((PACKAGE_ROOT / "setup.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "setup.cfg").is_file())
        self.assertTrue((PACKAGE_ROOT / "resource" / "robot_perception").is_file())
        self.assertTrue((PACKAGE_ROOT / "robot_perception" / "__init__.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "robot_perception" / "color_blob_detector.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "robot_perception" / "image_detector_node.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "config" / "color_detector.yaml").is_file())
        self.assertTrue((PACKAGE_ROOT / "launch" / "color_detector.launch.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "README.md").is_file())
        self.assertTrue((PACKAGE_ROOT / "WEEK_05_01_IMAGE_DETECTION_NODE.md").is_file())

    def test_setup_installs_launch_and_config_files(self):
        setup_path = PACKAGE_ROOT / "setup.py"
        if not setup_path.is_file():
            self.fail("robot_perception/setup.py should exist")

        setup_tree = ast.parse(setup_path.read_text(encoding="utf-8"))
        string_literals = {
            node.value
            for node in ast.walk(setup_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }

        self.assertIn("launch/*.launch.py", string_literals)
        self.assertIn("config/*.yaml", string_literals)
        self.assertIn("image_detector_node = robot_perception.image_detector_node:main", string_literals)

    def test_package_declares_image_detection_dependencies(self):
        package_path = PACKAGE_ROOT / "package.xml"
        if not package_path.is_file():
            self.fail("robot_perception/package.xml should exist")

        package_xml = ET.parse(package_path)
        dependencies = {
            element.text
            for element in package_xml.findall(".//depend")
        } | {
            element.text
            for element in package_xml.findall(".//exec_depend")
        }

        self.assertIn("cv_bridge", dependencies)
        self.assertIn("image_transport", dependencies)
        self.assertIn("launch", dependencies)
        self.assertIn("launch_ros", dependencies)
        self.assertIn("python3-opencv", dependencies)
        self.assertIn("rclpy", dependencies)
        self.assertIn("robot_interfaces", dependencies)
        self.assertIn("sensor_msgs", dependencies)

    def test_config_uses_camera_image_and_target_detection_topics(self):
        config_path = PACKAGE_ROOT / "config" / "color_detector.yaml"
        if not config_path.is_file():
            self.fail("robot_perception/config/color_detector.yaml should exist")

        config_text = config_path.read_text(encoding="utf-8")

        self.assertIn("image_topic: /camera/image_raw", config_text)
        self.assertIn("detection_topic: /target_detection", config_text)
        self.assertIn("debug_image_topic: /target_detection/debug_image", config_text)
        self.assertIn("target_color: red", config_text)
        self.assertIn("min_area_pixels: 200.0", config_text)
        self.assertIn("publish_debug_image: true", config_text)

    def test_launch_starts_image_detector_with_config(self):
        launch_path = PACKAGE_ROOT / "launch" / "color_detector.launch.py"
        if not launch_path.is_file():
            self.fail("robot_perception/launch/color_detector.launch.py should exist")

        launch_source = launch_path.read_text(encoding="utf-8")
        launch_tree = ast.parse(launch_source)
        string_literals = {
            node.value
            for node in ast.walk(launch_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }

        self.assertIn("robot_perception", string_literals)
        self.assertIn("image_detector_node", string_literals)
        self.assertIn("color_detector.yaml", string_literals)
        self.assertIn("use_sim_time", string_literals)

    def test_image_detector_node_uses_cv_bridge_sensor_qos_and_target_message(self):
        node_path = PACKAGE_ROOT / "robot_perception" / "image_detector_node.py"
        if not node_path.is_file():
            self.fail("robot_perception/robot_perception/image_detector_node.py should exist")

        node_source = node_path.read_text(encoding="utf-8")

        self.assertIn("CvBridge", node_source)
        self.assertIn("qos_profile_sensor_data", node_source)
        self.assertIn("TargetDetection", node_source)
        self.assertIn("detect_largest_color_blob", node_source)
        self.assertIn("draw_detection_box", node_source)


if __name__ == "__main__":
    unittest.main()
