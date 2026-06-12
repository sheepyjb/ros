import ast
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


class RobotSimulationAssetsTest(unittest.TestCase):
    """检查第 4 周 Gazebo 仿真包的基础资产。"""

    def test_package_files_exist(self):
        self.assertTrue((PACKAGE_ROOT / "package.xml").is_file())
        self.assertTrue((PACKAGE_ROOT / "setup.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "setup.cfg").is_file())
        self.assertTrue((PACKAGE_ROOT / "resource" / "robot_simulation").is_file())
        self.assertTrue((PACKAGE_ROOT / "robot_simulation" / "__init__.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "launch" / "gazebo_empty_world.launch.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "worlds" / "empty_diffbot.world.sdf").is_file())
        self.assertTrue((PACKAGE_ROOT / "config" / "clock_bridge.yaml").is_file())
        self.assertTrue((PACKAGE_ROOT / "WEEK_04_01_GAZEBO_ENVIRONMENT.md").is_file())

    def test_setup_installs_simulation_assets(self):
        setup_path = PACKAGE_ROOT / "setup.py"
        if not setup_path.is_file():
            self.fail("robot_simulation/setup.py should exist")

        setup_tree = ast.parse(setup_path.read_text(encoding="utf-8"))
        string_literals = {
            node.value
            for node in ast.walk(setup_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }

        self.assertIn("launch/*.launch.py", string_literals)
        self.assertIn("worlds/*.sdf", string_literals)
        self.assertIn("config/*.yaml", string_literals)

    def test_package_declares_gazebo_dependencies(self):
        package_path = PACKAGE_ROOT / "package.xml"
        if not package_path.is_file():
            self.fail("robot_simulation/package.xml should exist")

        package_xml = ET.parse(package_path)
        dependencies = {
            element.text
            for element in package_xml.findall(".//depend")
        } | {
            element.text
            for element in package_xml.findall(".//exec_depend")
        }

        self.assertIn("ament_index_python", dependencies)
        self.assertIn("launch", dependencies)
        self.assertIn("launch_ros", dependencies)
        self.assertIn("ros_gz_sim", dependencies)
        self.assertIn("ros_gz_bridge", dependencies)

    def test_empty_world_has_required_gazebo_systems(self):
        world_path = PACKAGE_ROOT / "worlds" / "empty_diffbot.world.sdf"
        if not world_path.is_file():
            self.fail("robot_simulation/worlds/empty_diffbot.world.sdf should exist")

        sdf = ET.parse(world_path).getroot()
        self.assertEqual("sdf", sdf.tag)

        world = sdf.find("world")
        self.assertIsNotNone(world)
        self.assertEqual("diffbot_empty_world", world.attrib["name"])

        plugin_filenames = {
            plugin.attrib["filename"]
            for plugin in world.findall("plugin")
        }
        self.assertIn("gz-sim-physics-system", plugin_filenames)
        self.assertIn("gz-sim-user-commands-system", plugin_filenames)
        self.assertIn("gz-sim-scene-broadcaster-system", plugin_filenames)
        self.assertIsNotNone(world.find("model[@name='ground_plane']"))

    def test_clock_bridge_config_is_gazebo_to_ros_only(self):
        config_path = PACKAGE_ROOT / "config" / "clock_bridge.yaml"
        if not config_path.is_file():
            self.fail("robot_simulation/config/clock_bridge.yaml should exist")

        config_text = config_path.read_text(encoding="utf-8")
        self.assertIn('ros_topic_name: "/clock"', config_text)
        self.assertIn('gz_topic_name: "/clock"', config_text)
        self.assertIn('ros_type_name: "rosgraph_msgs/msg/Clock"', config_text)
        self.assertIn('gz_type_name: "gz.msgs.Clock"', config_text)
        self.assertIn("direction: GZ_TO_ROS", config_text)

    def test_gazebo_launch_uses_ros_gz_sim_and_clock_bridge(self):
        launch_path = PACKAGE_ROOT / "launch" / "gazebo_empty_world.launch.py"
        if not launch_path.is_file():
            self.fail("robot_simulation/launch/gazebo_empty_world.launch.py should exist")

        launch_source = launch_path.read_text(encoding="utf-8")
        launch_tree = ast.parse(launch_source)
        string_literals = {
            node.value
            for node in ast.walk(launch_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }

        self.assertIn("ros_gz_sim", string_literals)
        self.assertIn("gz_sim.launch.py", string_literals)
        self.assertIn("empty_diffbot.world.sdf", string_literals)
        self.assertIn("ros_gz_bridge", string_literals)
        self.assertIn("parameter_bridge", string_literals)
        self.assertIn("clock_bridge.yaml", string_literals)


if __name__ == "__main__":
    unittest.main()
