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
        self.assertTrue((PACKAGE_ROOT / "launch" / "diffbot_drive.launch.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "worlds" / "empty_diffbot.world.sdf").is_file())
        self.assertTrue((PACKAGE_ROOT / "worlds" / "diffbot_drive.world.sdf").is_file())
        self.assertTrue((PACKAGE_ROOT / "config" / "clock_bridge.yaml").is_file())
        self.assertTrue((PACKAGE_ROOT / "config" / "diff_drive_bridge.yaml").is_file())
        self.assertTrue((PACKAGE_ROOT / "WEEK_04_01_GAZEBO_ENVIRONMENT.md").is_file())
        self.assertTrue((PACKAGE_ROOT / "WEEK_04_02_DIFFBOT_DRIVE_IN_GAZEBO.md").is_file())

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
        self.assertIn("geometry_msgs", dependencies)
        self.assertIn("launch", dependencies)
        self.assertIn("launch_ros", dependencies)
        self.assertIn("nav_msgs", dependencies)
        self.assertIn("ros_gz_sim", dependencies)
        self.assertIn("ros_gz_bridge", dependencies)
        self.assertIn("rosgraph_msgs", dependencies)

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

    def test_diffbot_drive_world_has_model_and_diff_drive_plugin(self):
        world_path = PACKAGE_ROOT / "worlds" / "diffbot_drive.world.sdf"
        if not world_path.is_file():
            self.fail("robot_simulation/worlds/diffbot_drive.world.sdf should exist")

        world = ET.parse(world_path).getroot().find("world")
        self.assertIsNotNone(world)
        self.assertEqual("diffbot_drive_world", world.attrib["name"])

        model = world.find("model[@name='diffbot']")
        self.assertIsNotNone(model)
        self.assertEqual("0 0 0 0 0 0", model.find("pose").text)

        links = {link.attrib["name"] for link in model.findall("link")}
        joints = {joint.attrib["name"]: joint for joint in model.findall("joint")}

        self.assertIn("base_link", links)
        self.assertIn("left_wheel_link", links)
        self.assertIn("right_wheel_link", links)

        self.assertEqual("0 0.18 0.07 0 0 0", model.find("link[@name='left_wheel_link']").find("pose").text)
        self.assertEqual("0 -0.18 0.07 0 0 0", model.find("link[@name='right_wheel_link']").find("pose").text)
        for wheel_name in ("left_wheel_link", "right_wheel_link"):
            wheel_link = model.find(f"link[@name='{wheel_name}']")
            self.assertEqual("0 0 0 1.5708 0 0", wheel_link.find("visual").find("pose").text)
            self.assertEqual("0 0 0 1.5708 0 0", wheel_link.find("collision").find("pose").text)

        self.assertEqual("revolute", joints["left_wheel_joint"].attrib["type"])
        self.assertEqual("revolute", joints["right_wheel_joint"].attrib["type"])
        self.assertEqual("base_link", joints["left_wheel_joint"].find("parent").text)
        self.assertEqual("left_wheel_link", joints["left_wheel_joint"].find("child").text)
        self.assertEqual("base_link", joints["right_wheel_joint"].find("parent").text)
        self.assertEqual("right_wheel_link", joints["right_wheel_joint"].find("child").text)
        self.assertEqual("0 1 0", joints["left_wheel_joint"].find("axis").find("xyz").text)
        self.assertEqual("0 1 0", joints["right_wheel_joint"].find("axis").find("xyz").text)

        plugin = model.find("plugin[@name='gz::sim::systems::DiffDrive']")
        self.assertIsNotNone(plugin)
        self.assertEqual("gz-sim-diff-drive-system", plugin.attrib["filename"])
        self.assertEqual("left_wheel_joint", plugin.find("left_joint").text)
        self.assertEqual("right_wheel_joint", plugin.find("right_joint").text)
        self.assertEqual("0.36", plugin.find("wheel_separation").text)
        self.assertEqual("0.07", plugin.find("wheel_radius").text)
        self.assertEqual("/cmd_vel", plugin.find("topic").text)
        self.assertEqual("/odom", plugin.find("odom_topic").text)
        self.assertEqual("odom", plugin.find("frame_id").text)
        self.assertEqual("base_link", plugin.find("child_frame_id").text)

    def test_diff_drive_bridge_config_connects_cmd_vel_and_odom(self):
        config_path = PACKAGE_ROOT / "config" / "diff_drive_bridge.yaml"
        if not config_path.is_file():
            self.fail("robot_simulation/config/diff_drive_bridge.yaml should exist")

        config_text = config_path.read_text(encoding="utf-8")

        self.assertIn('ros_topic_name: "/clock"', config_text)
        self.assertIn("direction: GZ_TO_ROS", config_text)
        self.assertIn('ros_topic_name: "/cmd_vel"', config_text)
        self.assertIn('gz_topic_name: "/cmd_vel"', config_text)
        self.assertIn('ros_type_name: "geometry_msgs/msg/Twist"', config_text)
        self.assertIn('gz_type_name: "gz.msgs.Twist"', config_text)
        self.assertIn("direction: ROS_TO_GZ", config_text)
        self.assertIn('ros_topic_name: "/odom"', config_text)
        self.assertIn('gz_topic_name: "/odom"', config_text)
        self.assertIn('ros_type_name: "nav_msgs/msg/Odometry"', config_text)
        self.assertIn('gz_type_name: "gz.msgs.Odometry"', config_text)

    def test_diffbot_drive_launch_uses_drive_world_and_bridge_config(self):
        launch_path = PACKAGE_ROOT / "launch" / "diffbot_drive.launch.py"
        if not launch_path.is_file():
            self.fail("robot_simulation/launch/diffbot_drive.launch.py should exist")

        launch_source = launch_path.read_text(encoding="utf-8")
        launch_tree = ast.parse(launch_source)
        string_literals = {
            node.value
            for node in ast.walk(launch_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }

        self.assertIn("ros_gz_sim", string_literals)
        self.assertIn("gz_sim.launch.py", string_literals)
        self.assertIn("diffbot_drive.world.sdf", string_literals)
        self.assertIn("ros_gz_bridge", string_literals)
        self.assertIn("parameter_bridge", string_literals)
        self.assertIn("diff_drive_bridge.yaml", string_literals)


if __name__ == "__main__":
    unittest.main()
