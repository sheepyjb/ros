import ast  # 用 Python 语法树检查 setup.py，而不是靠脆弱的字符串切片。
import unittest
import xml.etree.ElementTree as ET  # 用标准 XML 解析器读取 package.xml。
from pathlib import Path  # 用 pathlib 定位当前测试文件所在的包根目录。


# __file__ 是当前测试文件路径。
# parents[1] 表示从 test/test_perception_assets.py 回到 robot_perception 包根目录。
PACKAGE_ROOT = Path(__file__).resolve().parents[1]


class RobotPerceptionAssetsTest(unittest.TestCase):
    """检查第 5 周第 1 小课的感知包资产。"""

    def test_package_files_exist(self):
        # 这组断言保证包的基本结构完整。
        # 如果某个文件被误删，测试会直接指出缺哪个文件。
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

        # ast.parse 会把 setup.py 解析成语法树。
        # 这样可以找出 setup.py 里出现过的字符串字面量，检查安装声明是否存在。
        setup_tree = ast.parse(setup_path.read_text(encoding="utf-8"))
        string_literals = {
            node.value
            for node in ast.walk(setup_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }

        # launch/config 文件必须通过 data_files 安装，否则 ros2 launch 会在 install/ 下找不到它们。
        self.assertIn("launch/*.launch.py", string_literals)
        self.assertIn("config/*.yaml", string_literals)
        self.assertIn("image_detector_node = robot_perception.image_detector_node:main", string_literals)

    def test_package_declares_image_detection_dependencies(self):
        package_path = PACKAGE_ROOT / "package.xml"
        if not package_path.is_file():
            self.fail("robot_perception/package.xml should exist")

        package_xml = ET.parse(package_path)

        # package.xml 可能使用 <depend> 或 <exec_depend>，这里统一收集。
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

        # 这里只做轻量检查：确认默认话题名和关键参数在 YAML 中存在。
        # 不引入额外 YAML 解析库，保持测试对初学者更直观。
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

        # launch 文件应该启动 robot_perception 包里的 image_detector_node，并加载默认 YAML。
        self.assertIn("robot_perception", string_literals)
        self.assertIn("image_detector_node", string_literals)
        self.assertIn("color_detector.yaml", string_literals)
        self.assertIn("use_sim_time", string_literals)

    def test_image_detector_node_uses_cv_bridge_sensor_qos_and_target_message(self):
        node_path = PACKAGE_ROOT / "robot_perception" / "image_detector_node.py"
        if not node_path.is_file():
            self.fail("robot_perception/robot_perception/image_detector_node.py should exist")

        node_source = node_path.read_text(encoding="utf-8")

        # 这组断言锁定节点的核心链路：
        # CvBridge 转图像、sensor QoS 订阅、TargetDetection 发布、检测和画框函数。
        self.assertIn("CvBridge", node_source)
        self.assertIn("qos_profile_sensor_data", node_source)
        self.assertIn("TargetDetection", node_source)
        self.assertIn("detect_largest_color_blob", node_source)
        self.assertIn("draw_detection_box", node_source)


if __name__ == "__main__":
    unittest.main()
