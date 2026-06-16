import os
from glob import glob

from setuptools import setup


package_name = "robot_simulation"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        (os.path.join("share", package_name), ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "worlds"), glob("worlds/*.sdf")),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (
            os.path.join("share", package_name, "materials", "textures"),
            glob("materials/textures/*.png"),
        ),
        (os.path.join("share", package_name, "rviz"), glob("rviz/*.rviz")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="ROS 2 Learner",
    maintainer_email="student@example.com",
    description="Gazebo simulation assets for the ROS 2 learning robot.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "odom_to_tf = robot_simulation.odom_to_tf:main",
        ],
    },
)
