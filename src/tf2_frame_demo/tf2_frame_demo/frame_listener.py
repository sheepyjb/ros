import rclpy  # ROS 2 Python 客户端库，负责初始化、创建节点和 spin。
from rclpy.node import Node  # 所有 rclpy 节点类都继承自 Node。
from rclpy.time import Time  # lookup_transform 查询时间会用到 Time。
from tf2_ros import Buffer  # Buffer 保存 listener 收到的 TF 数据。
from tf2_ros import TransformException  # 查询 TF 失败时抛出的异常类型。
from tf2_ros import TransformListener  # 订阅 /tf 和 /tf_static，并把数据写入 Buffer。

from tf2_frame_demo.frame_math import quaternion_to_yaw


class FrameListener(Node):
    """查询 source_frame 在 target_frame 下的位置。"""

    def __init__(self):
        super().__init__("frame_listener")  # 节点名会显示在 ros2 node list 中。
        self.declare_parameter("target_frame", "map")  # 查询目标坐标系：希望把结果表达在 map 下。
        self.declare_parameter("source_frame", "camera_link")  # 被查询坐标系：摄像头坐标系。

        self._buffer = Buffer()  # 缓存收到的 TF 树。
        # TransformListener 会订阅 /tf 和 /tf_static，并持续把 transform 放进 buffer。
        self._listener = TransformListener(self._buffer, self)
        self.create_timer(0.5, self.lookup_transform)  # 每 0.5 秒查询一次 TF。

    def lookup_transform(self):
        target_frame = self.get_parameter("target_frame").value  # 一般是 map。
        source_frame = self.get_parameter("source_frame").value  # 一般是 camera_link。

        try:
            transform = self._buffer.lookup_transform(
                target_frame,  # 结果要表达在哪个坐标系下。
                source_frame,  # 想查询哪个坐标系的位置。
                Time(),  # Time() 表示查询 buffer 中最新可用的 transform。
            )
        except TransformException as exc:
            # launch 刚启动时，TF 数据可能还没进入 buffer。
            # 这时不要崩溃，只提示“正在等待 transform”。
            self.get_logger().info(
                f"Waiting for transform {target_frame} -> {source_frame}: {exc}"
            )
            return

        translation = transform.transform.translation  # camera_link 在 map 下的位置。
        yaw = quaternion_to_yaw(transform.transform.rotation)  # 把四元数转成更好读的 yaw。
        self.get_logger().info(
            f"{target_frame} -> {source_frame}: "
            f"x={translation.x:.2f}, y={translation.y:.2f}, yaw={yaw:.2f}"
        )


def main(args=None):
    rclpy.init(args=args)  # 初始化 ROS 2 Python 运行环境。
    node = FrameListener()  # 创建 TF 查询节点。
    try:
        rclpy.spin(node)  # 持续运行节点，让 timer 周期触发 lookup_transform。
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
