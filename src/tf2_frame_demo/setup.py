import os
from glob import glob

from setuptools import setup


package_name = "tf2_frame_demo"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        (os.path.join("share", package_name), ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="ROS 2 Learner",
    maintainer_email="student@example.com",
    description="ROS 2 tf2 frame learning demo.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "dynamic_frame_broadcaster = tf2_frame_demo.dynamic_frame_broadcaster:main",
            "frame_listener = tf2_frame_demo.frame_listener:main",
        ],
    },
)
