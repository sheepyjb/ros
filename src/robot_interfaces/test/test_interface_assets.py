import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


class InterfaceAssetsTest(unittest.TestCase):
    """检查自定义接口包是否包含第 2 周第 3 节需要的 msg 和 srv。"""

    def test_interface_files_exist(self):
        self.assertTrue((PACKAGE_ROOT / "package.xml").is_file())
        self.assertTrue((PACKAGE_ROOT / "CMakeLists.txt").is_file())
        self.assertTrue((PACKAGE_ROOT / "msg" / "TargetDetection.msg").is_file())
        self.assertTrue((PACKAGE_ROOT / "srv" / "SetGoal.srv").is_file())

    def test_target_detection_message_fields(self):
        message_path = PACKAGE_ROOT / "msg" / "TargetDetection.msg"
        if not message_path.is_file():
            self.fail("robot_interfaces/msg/TargetDetection.msg should exist")

        fields = message_path.read_text(encoding="utf-8").splitlines()

        self.assertIn("string label", fields)
        self.assertIn("float32 confidence", fields)
        self.assertIn("float32 center_x", fields)
        self.assertIn("float32 center_y", fields)
        self.assertIn("float32 width", fields)
        self.assertIn("float32 height", fields)
        self.assertIn("bool is_tracking", fields)

    def test_set_goal_service_fields(self):
        service_path = PACKAGE_ROOT / "srv" / "SetGoal.srv"
        if not service_path.is_file():
            self.fail("robot_interfaces/srv/SetGoal.srv should exist")

        service_definition = service_path.read_text(encoding="utf-8")

        self.assertIn("float64 x", service_definition)
        self.assertIn("float64 y", service_definition)
        self.assertIn("---", service_definition)
        self.assertIn("bool success", service_definition)
        self.assertIn("string message", service_definition)

    def test_package_declares_interface_dependencies(self):
        package_path = PACKAGE_ROOT / "package.xml"
        if not package_path.is_file():
            self.fail("robot_interfaces/package.xml should exist")

        package_xml = ET.parse(package_path)
        dependency_tags = {
            element.tag: element.text
            for element in package_xml.iter()
            if element.text
        }
        all_dependencies = set(dependency_tags.values())

        self.assertIn("ament_cmake", all_dependencies)
        self.assertIn("rosidl_default_generators", all_dependencies)
        self.assertIn("rosidl_default_runtime", all_dependencies)
        self.assertIn("rosidl_interface_packages", all_dependencies)


if __name__ == "__main__":
    unittest.main()
