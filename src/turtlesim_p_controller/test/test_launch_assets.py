import ast
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


class LaunchAssetsTest(unittest.TestCase):
    """检查 launch 和参数文件是否作为 ROS 2 package 资产存在并会被安装。"""

    def test_launch_and_config_files_exist(self):
        self.assertTrue(
            (PACKAGE_ROOT / "launch" / "turtlesim_goal.launch.py").is_file()
        )
        self.assertTrue((PACKAGE_ROOT / "config" / "goal_controller.yaml").is_file())

    def test_setup_installs_launch_and_config_files(self):
        setup_tree = ast.parse((PACKAGE_ROOT / "setup.py").read_text(encoding="utf-8"))
        string_literals = {
            node.value
            for node in ast.walk(setup_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }

        self.assertIn("launch/*.launch.py", string_literals)
        self.assertIn("config/*.yaml", string_literals)


if __name__ == "__main__":
    unittest.main()
