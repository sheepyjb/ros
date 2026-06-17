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
        self.assertTrue((PACKAGE_ROOT / "launch" / "diffbot_sensors_rviz.launch.py").is_file())
        self.assertTrue((PACKAGE_ROOT / "worlds" / "empty_diffbot.world.sdf").is_file())
        self.assertTrue((PACKAGE_ROOT / "worlds" / "diffbot_drive.world.sdf").is_file())
        self.assertTrue((PACKAGE_ROOT / "worlds" / "diffbot_sensors.world.sdf").is_file())
        self.assertTrue((PACKAGE_ROOT / "config" / "clock_bridge.yaml").is_file())
        self.assertTrue((PACKAGE_ROOT / "config" / "diff_drive_bridge.yaml").is_file())
        self.assertTrue((PACKAGE_ROOT / "config" / "sensor_bridge.yaml").is_file())
        self.assertTrue((PACKAGE_ROOT / "materials" / "textures" / "yolo_stop_sign.png").is_file())
        self.assertTrue((PACKAGE_ROOT / "models" / "yolo_stop_sign_board" / "meshes" / "stop_sign_board.obj").is_file())
        self.assertTrue((PACKAGE_ROOT / "models" / "yolo_stop_sign_board" / "meshes" / "stop_sign_board.mtl").is_file())
        self.assertTrue((PACKAGE_ROOT / "rviz" / "sensors.rviz").is_file())
        self.assertTrue((PACKAGE_ROOT / "WEEK_04_01_GAZEBO_ENVIRONMENT.md").is_file())
        self.assertTrue((PACKAGE_ROOT / "WEEK_04_02_DIFFBOT_DRIVE_IN_GAZEBO.md").is_file())
        self.assertTrue((PACKAGE_ROOT / "WEEK_04_03_SENSORS_TF_RVIZ.md").is_file())

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
        self.assertIn("materials/textures/*.png", string_literals)
        self.assertIn("models/yolo_stop_sign_board/meshes/*.obj", string_literals)
        self.assertIn("models/yolo_stop_sign_board/meshes/*.mtl", string_literals)
        self.assertIn("rviz/*.rviz", string_literals)

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
        self.assertIn("robot_description", dependencies)
        self.assertIn("robot_state_publisher", dependencies)
        self.assertIn("ros_gz_sim", dependencies)
        self.assertIn("ros_gz_bridge", dependencies)
        self.assertIn("rosgraph_msgs", dependencies)
        self.assertIn("rviz2", dependencies)
        self.assertIn("sensor_msgs", dependencies)
        self.assertIn("teleop_twist_keyboard", dependencies)
        self.assertIn("tf2_ros", dependencies)
        self.assertIn("xacro", dependencies)

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
        self.assertIn("front_caster_link", links)
        self.assertIn("rear_caster_link", links)

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
        self.assertEqual("0.16 0 0.035 0 0 0", model.find("link[@name='front_caster_link']").find("pose").text)
        self.assertEqual("-0.16 0 0.035 0 0 0", model.find("link[@name='rear_caster_link']").find("pose").text)
        self.assertEqual("ball", joints["front_caster_joint"].attrib["type"])
        self.assertEqual("ball", joints["rear_caster_joint"].attrib["type"])
        self.assertEqual("base_link", joints["front_caster_joint"].find("parent").text)
        self.assertEqual("front_caster_link", joints["front_caster_joint"].find("child").text)
        self.assertEqual("base_link", joints["rear_caster_joint"].find("parent").text)
        self.assertEqual("rear_caster_link", joints["rear_caster_joint"].find("child").text)

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

    def test_sensor_world_adds_camera_lidar_and_scene_targets(self):
        world_path = PACKAGE_ROOT / "worlds" / "diffbot_sensors.world.sdf"
        if not world_path.is_file():
            self.fail("robot_simulation/worlds/diffbot_sensors.world.sdf should exist")

        world = ET.parse(world_path).getroot().find("world")
        self.assertIsNotNone(world)
        self.assertEqual("diffbot_sensors_world", world.attrib["name"])

        model = world.find("model[@name='diffbot']")
        self.assertIsNotNone(model)
        self.assertEqual("-0.45 0 0 0 0 0", model.find("pose").text)

        links = {link.attrib["name"] for link in model.findall("link")}
        self.assertIn("base_link", links)
        self.assertIn("laser_link", links)
        self.assertIn("camera_link", links)
        self.assertIn("front_caster_link", links)
        self.assertIn("rear_caster_link", links)

        joints = {joint.attrib["name"]: joint for joint in model.findall("joint")}
        self.assertEqual("0.16 0 0.035 0 0 0", model.find("link[@name='front_caster_link']").find("pose").text)
        self.assertEqual("-0.16 0 0.035 0 0 0", model.find("link[@name='rear_caster_link']").find("pose").text)
        self.assertEqual("ball", joints["front_caster_joint"].attrib["type"])
        self.assertEqual("ball", joints["rear_caster_joint"].attrib["type"])
        self.assertEqual("base_link", joints["front_caster_joint"].find("parent").text)
        self.assertEqual("front_caster_link", joints["front_caster_joint"].find("child").text)
        self.assertEqual("base_link", joints["rear_caster_joint"].find("parent").text)
        self.assertEqual("rear_caster_link", joints["rear_caster_joint"].find("child").text)

        laser_link = model.find("link[@name='laser_link']")
        laser_sensor = laser_link.find("sensor[@name='front_lidar']")
        self.assertIsNotNone(laser_sensor)
        self.assertEqual("gpu_lidar", laser_sensor.attrib["type"])
        self.assertEqual("/scan", laser_sensor.find("topic").text)
        self.assertEqual("10", laser_sensor.find("update_rate").text)
        self.assertEqual("360", laser_sensor.find("lidar/scan/horizontal/samples").text)
        self.assertEqual("-1.5708", laser_sensor.find("lidar/scan/horizontal/min_angle").text)
        self.assertEqual("1.5708", laser_sensor.find("lidar/scan/horizontal/max_angle").text)

        camera_link = model.find("link[@name='camera_link']")
        camera_sensor = camera_link.find("sensor[@name='front_camera']")
        self.assertIsNotNone(camera_sensor)
        self.assertEqual("camera", camera_sensor.attrib["type"])
        self.assertEqual("/camera/image_raw", camera_sensor.find("topic").text)
        self.assertEqual("15", camera_sensor.find("update_rate").text)
        self.assertEqual("/camera/camera_info", camera_sensor.find("camera/camera_info_topic").text)
        self.assertEqual("camera_optical_frame", camera_sensor.find("camera/optical_frame_id").text)

        obstacle_names = {model.attrib["name"] for model in world.findall("model")}
        self.assertIn("front_box", obstacle_names)
        self.assertIn("left_cylinder", obstacle_names)
        self.assertIn("yolo_stop_sign_board", obstacle_names)

        stop_sign = world.find("model[@name='yolo_stop_sign_board']")
        self.assertIsNotNone(stop_sign)
        self.assertEqual("true", stop_sign.find("static").text)
        self.assertEqual("1.35 0 0.60 0 0 0", stop_sign.find("pose").text)

        stop_sign_link = stop_sign.find("link[@name='sign_link']")
        self.assertIsNotNone(stop_sign_link)
        stop_sign_visual = stop_sign_link.find("visual[@name='stop_sign_visual']")
        self.assertIsNotNone(stop_sign_visual)
        self.assertEqual(
            "package://robot_simulation/models/yolo_stop_sign_board/meshes/stop_sign_board.obj",
            stop_sign_visual.find("geometry/mesh/uri").text,
        )

        mesh_material = PACKAGE_ROOT / "models" / "yolo_stop_sign_board" / "meshes" / "stop_sign_board.mtl"
        self.assertIn("map_Kd ../../../materials/textures/yolo_stop_sign.png", mesh_material.read_text(encoding="utf-8"))

    def test_sensor_bridge_connects_motion_sensor_and_tf_topics(self):
        config_path = PACKAGE_ROOT / "config" / "sensor_bridge.yaml"
        if not config_path.is_file():
            self.fail("robot_simulation/config/sensor_bridge.yaml should exist")

        config_text = config_path.read_text(encoding="utf-8")

        self.assertIn('ros_topic_name: "/clock"', config_text)
        self.assertIn('ros_topic_name: "/cmd_vel"', config_text)
        self.assertIn('ros_topic_name: "/odom"', config_text)
        self.assertIn('ros_topic_name: "/scan"', config_text)
        self.assertIn('ros_topic_name: "/camera/image_raw"', config_text)
        self.assertIn('ros_topic_name: "/camera/camera_info"', config_text)
        self.assertIn('ros_type_name: "sensor_msgs/msg/LaserScan"', config_text)
        self.assertIn('ros_type_name: "sensor_msgs/msg/Image"', config_text)
        self.assertIn('ros_type_name: "sensor_msgs/msg/CameraInfo"', config_text)
        self.assertIn('gz_type_name: "gz.msgs.LaserScan"', config_text)
        self.assertIn('gz_type_name: "gz.msgs.Image"', config_text)
        self.assertIn('gz_type_name: "gz.msgs.CameraInfo"', config_text)
        self.assertIn('frame_id: "laser_link"', config_text)
        self.assertIn('frame_id: "camera_optical_frame"', config_text)
        self.assertNotIn("qos_profile: SENSOR_DATA", config_text)

    def test_sensor_rviz_config_shows_robot_tf_scan_and_camera(self):
        rviz_path = PACKAGE_ROOT / "rviz" / "sensors.rviz"
        if not rviz_path.is_file():
            self.fail("robot_simulation/rviz/sensors.rviz should exist")

        rviz_text = rviz_path.read_text(encoding="utf-8")

        self.assertIn("Fixed Frame: odom", rviz_text)
        self.assertIn("Class: rviz_default_plugins/RobotModel", rviz_text)
        self.assertIn("Class: rviz_default_plugins/TF", rviz_text)
        self.assertIn("Class: rviz_default_plugins/LaserScan", rviz_text)
        self.assertIn("Topic: /scan", rviz_text)
        self.assertIn("Class: rviz_default_plugins/Image", rviz_text)
        self.assertIn("Topic: /camera/image_raw", rviz_text)
        self.assertIn("Durability Policy: Transient Local", rviz_text)

    def test_sensor_launch_starts_gazebo_bridge_tf_model_and_rviz(self):
        launch_path = PACKAGE_ROOT / "launch" / "diffbot_sensors_rviz.launch.py"
        if not launch_path.is_file():
            self.fail("robot_simulation/launch/diffbot_sensors_rviz.launch.py should exist")

        launch_source = launch_path.read_text(encoding="utf-8")
        launch_tree = ast.parse(launch_source)
        string_literals = {
            node.value
            for node in ast.walk(launch_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }

        self.assertIn("ros_gz_sim", string_literals)
        self.assertIn("gz_sim.launch.py", string_literals)
        self.assertIn("diffbot_sensors.world.sdf", string_literals)
        self.assertIn("sensor_bridge.yaml", string_literals)
        self.assertIn("robot_description", string_literals)
        self.assertIn("diffbot.urdf.xacro", string_literals)
        self.assertIn("robot_state_publisher", string_literals)
        self.assertIn("odom_to_tf", string_literals)
        self.assertIn("rviz2", string_literals)
        self.assertIn("sensors.rviz", string_literals)
        self.assertIn("package://robot_simulation/models/yolo_stop_sign_board/meshes/stop_sign_board.obj", string_literals)
        self.assertIn("on_exit_shutdown", string_literals)
        self.assertIn("false", string_literals)
        self.assertIn("diffbot_sensors.resolved.world.sdf", string_literals)
        self.assertIn("file://", launch_source)
        self.assertIn("as_posix", launch_source)

    def test_week_04_03_documents_direct_interactive_keyboard_teleop(self):
        lesson_path = PACKAGE_ROOT / "WEEK_04_03_SENSORS_TF_RVIZ.md"
        if not lesson_path.is_file():
            self.fail("robot_simulation/WEEK_04_03_SENSORS_TF_RVIZ.md should exist")

        lesson_text = lesson_path.read_text(encoding="utf-8")

        self.assertIn("ros2 run teleop_twist_keyboard teleop_twist_keyboard", lesson_text)
        self.assertIn("真正的交互终端", lesson_text)
        self.assertIn("/cmd_vel", lesson_text)
        self.assertIn("i      前进", lesson_text)


if __name__ == "__main__":
    unittest.main()
