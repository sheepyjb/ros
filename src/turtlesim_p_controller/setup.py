from setuptools import setup


package_name = "turtlesim_p_controller"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="ROS 2 Learner",
    maintainer_email="student@example.com",
    description="ROS 2 turtlesim P 控制学习练习。",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "turtle_goal_controller = turtlesim_p_controller.turtle_goal_controller:main",
        ],
    },
)
