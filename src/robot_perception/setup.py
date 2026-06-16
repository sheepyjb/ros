import os  # 用来拼接跨平台路径，例如 share/robot_perception/launch。
from glob import glob  # 用通配符一次收集 launch/*.launch.py、config/*.yaml。

from setuptools import setup  # ament_python 包最终也是用 setuptools 安装 Python 代码。


package_name = "robot_perception"  # ROS 2 包名，也对应 Python import 的包目录名。

setup(
    name=package_name,  # 安装包名称，colcon build 时会使用。
    version="0.1.0",
    packages=[package_name],  # 要安装的 Python package：robot_perception/。
    data_files=[
        # 这一行会在 ament index 中注册包名。
        # 没有它，ros2 pkg prefix robot_perception 可能找不到这个包。
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),

        # package.xml 会安装到 install/robot_perception/share/robot_perception/package.xml。
        (os.path.join("share", package_name), ["package.xml"]),

        # launch 和 config 都不是 Python import 文件，而是运行时资产。
        # 必须安装到 share 目录，ros2 launch 才能在 install/ 下找到它们。
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],  # Python 打包工具依赖。
    zip_safe=True,  # 允许以 zip 形式安装；ROS 2 示例包通常保留这个字段。
    maintainer="ROS 2 Learner",
    maintainer_email="student@example.com",
    description="ROS 2 image perception exercises for the learning robot.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            # 这行定义 ros2 run 能看到的可执行入口：
            # ros2 run robot_perception image_detector_node
            # 会调用 robot_perception/image_detector_node.py 里的 main()。
            "image_detector_node = robot_perception.image_detector_node:main",
        ],
    },
)
