import rclpy  # ROS 2 Python 客户端库，负责初始化、创建节点和 spin。
from geometry_msgs.msg import TransformStamped  # TF 单条坐标变换使用的消息类型。
from rclpy.node import Node  # 所有 rclpy 节点类都继承自 Node。
from tf2_ros import TransformBroadcaster  # 用来发布动态 TF 到 /tf。

from tf2_frame_demo.frame_math import circular_pose  # 计算 base_link 绕圆运动时的 x/y/yaw。
from tf2_frame_demo.frame_math import yaw_to_quaternion  # 把 yaw 转成 TF 需要的四元数。


class DynamicFrameBroadcaster(Node):
    """发布 odom -> base_link 的动态坐标变换。"""

    def __init__(self):
        super().__init__("dynamic_frame_broadcaster")  # 节点名会显示在 ros2 node list 中。
        self.declare_parameter("parent_frame", "odom")  # 父坐标系：里程计坐标系。
        self.declare_parameter("child_frame", "base_link")  # 子坐标系：机器人底盘坐标系。
        self.declare_parameter("radius", 1.5)  # 模拟圆周运动半径，单位是米。
        self.declare_parameter("angular_speed", 0.4)  # 模拟圆周运动角速度，单位 rad/s。

        self._broadcaster = TransformBroadcaster(self)  # 后续通过它把 TransformStamped 发到 /tf。
        self._start_time = self.get_clock().now()  # 记录启动时刻，用来计算已经运动了多久。
        self.create_timer(0.05, self.broadcast_transform)  # 每 0.05 秒发布一次动态 TF。

    def broadcast_transform(self):
        now = self.get_clock().now()  # 当前 ROS 时间。
        # rclpy 的时间差是纳秒，这里换算成秒，方便代入圆周运动公式。
        elapsed = (now - self._start_time).nanoseconds / 1_000_000_000.0

        radius = self.get_parameter("radius").value  # 当前圆周半径参数。
        angular_speed = self.get_parameter("angular_speed").value  # 当前角速度参数。
        # 纯数学函数负责计算 base_link 在 odom 下的 x/y/yaw。
        pose = circular_pose(elapsed, radius=radius, angular_speed=angular_speed)
        quaternion = yaw_to_quaternion(pose.yaw)  # TF 需要四元数，所以把 yaw 转成 quaternion。

        transform = TransformStamped()  # 一条带时间戳的坐标变换。
        transform.header.stamp = now.to_msg()  # TF 需要知道这条变换对应哪个时刻。
        # header.frame_id 是父坐标系，这里表示“在 odom 坐标系下描述 base_link”。
        transform.header.frame_id = self.get_parameter("parent_frame").value
        # child_frame_id 是子坐标系，这里就是正在运动的机器人底盘。
        transform.child_frame_id = self.get_parameter("child_frame").value
        transform.transform.translation.x = pose.x  # base_link 在 odom 下的 x 位置。
        transform.transform.translation.y = pose.y  # base_link 在 odom 下的 y 位置。
        transform.transform.translation.z = 0.0  # 本课只做平面运动，所以 z 固定为 0。
        transform.transform.rotation.x = quaternion.x  # 姿态四元数 x 分量。
        transform.transform.rotation.y = quaternion.y  # 姿态四元数 y 分量。
        transform.transform.rotation.z = quaternion.z  # 姿态四元数 z 分量。
        transform.transform.rotation.w = quaternion.w  # 姿态四元数 w 分量。

        self._broadcaster.sendTransform(transform)  # 发布 odom -> base_link 动态 TF。


def main(args=None):
    rclpy.init(args=args)  # 初始化 ROS 2 Python 运行环境。
    node = DynamicFrameBroadcaster()  # 创建动态 TF 发布节点。
    try:
        rclpy.spin(node)  # 持续运行节点，让 timer 周期触发 broadcast_transform。
    except KeyboardInterrupt:
        pass  # 用户 Ctrl-C 停止 launch 时，安静退出。
    finally:
        try:
            node.destroy_node()  # 销毁节点，释放 ROS 2 资源。
        except KeyboardInterrupt:
            pass  # 如果清理过程中再次收到 Ctrl-C，也保持安静退出。
        if rclpy.ok():
            rclpy.shutdown()  # 只有 context 还没关闭时才调用，避免重复 shutdown 报错。


if __name__ == "__main__":
    main()
