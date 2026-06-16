import rclpy  # ROS 2 Python 客户端库，负责初始化、创建节点和 spin。
from cv_bridge import CvBridge  # 在 sensor_msgs/Image 和 OpenCV 图像之间转换。
from rclpy.node import Node  # 所有 rclpy 节点都继承 Node。
from rclpy.qos import qos_profile_sensor_data  # 适合相机/雷达这类高频传感器数据。
from robot_interfaces.msg import TargetDetection  # 第 2 周定义的检测结果消息。
from sensor_msgs.msg import Image  # ROS 2 标准图像消息类型。

from robot_perception.color_blob_detector import (
    DetectionResult,
    detect_largest_color_blob,
    draw_detection_box,
)
from robot_perception.yolo_detector import YoloObjectDetector


class ImageDetectorNode(Node):
    """订阅相机图像，运行颜色检测，并发布检测结果和调试图像。"""

    def __init__(self):
        super().__init__("image_detector_node")  # 节点名会显示在 ros2 node list 中。

        # 参数先声明，再从 YAML 或 launch 覆盖。这样同一个节点可以换输入话题、
        # 输出话题、目标颜色和面积阈值，不需要改 Python 源码。
        # declare_parameter 的作用是“告诉 ROS 2：这个节点有一个叫 image_topic 的参数”。
        # 第二个值是默认值；如果 YAML 或 launch 没覆盖，就用这个默认值。
        self.declare_parameter("image_topic", "/camera/image_raw")  # 输入图像话题。
        self.declare_parameter("detection_topic", "/target_detection")  # 检测结果输出话题。
        self.declare_parameter(
            "debug_image_topic",
            "/target_detection/debug_image",
        )  # 画了检测框的调试图像话题。
        self.declare_parameter("target_color", "red")  # 默认检测红色目标。
        self.declare_parameter("min_area_pixels", 200.0)  # 小于这个面积的目标当成噪声。
        self.declare_parameter("publish_debug_image", True)  # 是否发布调试图像。
        self.declare_parameter("detector_backend", "color")  # color 或 yolo。
        self.declare_parameter("yolo_model_path", "yolov8n.pt")  # YOLO 权重路径或模型名。
        self.declare_parameter("yolo_confidence_threshold", 0.25)  # YOLO 最小置信度。
        self.declare_parameter("yolo_target_class", "")  # 空字符串表示接受任意类别。

        # get_parameter(...).value 会读取最终参数值：
        # 优先级大致是 launch 命令行覆盖 > YAML 文件 > declare_parameter 默认值。
        # target_color/min_area_pixels/publish_debug_image 后续每帧图像都会用到，
        # 所以保存成 self.xxx 成员变量，image_callback() 里可以直接访问。
        self.target_color = self.get_parameter("target_color").value
        self.min_area_pixels = float(self.get_parameter("min_area_pixels").value)
        self.publish_debug_image = bool(self.get_parameter("publish_debug_image").value)
        self.detector_backend = self.get_parameter("detector_backend").value
        self.yolo_detector = self._create_yolo_detector()

        # 这三个话题名只在创建 subscriber/publisher 时用一次，
        # 所以用局部变量即可，不需要保存成 self.image_topic。
        image_topic = self.get_parameter("image_topic").value
        detection_topic = self.get_parameter("detection_topic").value
        debug_image_topic = self.get_parameter("debug_image_topic").value

        # CvBridge 只负责格式转换，不做算法：ROS Image <-> OpenCV BGR 图像。
        self.bridge = CvBridge()

        # /target_detection 是给后续控制、跟踪或日志节点使用的结构化检测结果。
        self.detection_publisher = self.create_publisher(
            TargetDetection,  # 发布的消息类型，对应 robot_interfaces/msg/TargetDetection。
            detection_topic,  # 发布到哪个话题，默认 /target_detection。
            10,  # 队列深度：订阅者短暂来不及处理时，最多缓存 10 条消息。
        )

        # /target_detection/debug_image 是给人看的调试图像，RViz2 Image display 可以订阅。
        self.debug_image_publisher = self.create_publisher(
            Image,  # 发布的消息类型，仍然是 ROS 2 标准图像消息。
            debug_image_topic,  # 发布到哪个话题，默认 /target_detection/debug_image。
            10,
        )

        # 图像订阅使用 sensor data QoS，更适合“关注最新帧”的实时传感器话题。
        self.image_subscription = self.create_subscription(
            Image,  # 订阅的消息类型，对应 sensor_msgs/msg/Image。
            image_topic,  # 订阅哪个话题，默认 /camera/image_raw。
            self.image_callback,  # 每收到一帧图像，就调用这个函数处理。
            qos_profile_sensor_data,  # 使用传感器 QoS，和 Gazebo bridge 的图像话题更匹配。
        )

    def image_callback(self, image_msg: Image) -> None:
        try:
            # desired_encoding="bgr8" 表示转成 OpenCV 常用的 8 位 BGR 彩色图。
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, desired_encoding="bgr8")
        except Exception as exc:
            # 图像编码不兼容时不要让节点崩溃，记录警告后等待下一帧。
            self.get_logger().warning(f"无法把 ROS Image 转成 OpenCV 图像：{exc}")
            return

        detection = self._detect_image(cv_image)

        # 结构化结果发给 /target_detection，后续第 6 周控制节点会用这个话题。
        self.detection_publisher.publish(detection_to_message(detection))

        if not self.publish_debug_image:
            return

        # debug 图像只用于可视化，不影响 /target_detection 的数据。
        debug_image = draw_detection_box(cv_image, detection)
        debug_msg = self.bridge.cv2_to_imgmsg(debug_image, encoding="bgr8")

        # 保留原始图像 header，尤其是 stamp 和 frame_id，方便 RViz2 和 rosbag 对齐时间。
        debug_msg.header = image_msg.header
        self.debug_image_publisher.publish(debug_msg)

    def _create_yolo_detector(self):
        if self.detector_backend == "color":
            return None

        if self.detector_backend != "yolo":
            raise ValueError(f"Unsupported detector_backend: {self.detector_backend}")

        return YoloObjectDetector(
            model_path=self.get_parameter("yolo_model_path").value,
            confidence_threshold=float(self.get_parameter("yolo_confidence_threshold").value),
            target_class=self.get_parameter("yolo_target_class").value,
        )

    def _detect_image(self, cv_image) -> DetectionResult:
        if self.detector_backend == "yolo":
            return self.yolo_detector.detect(cv_image)

        # color 后端保留第 1 小课行为，作为无模型 fallback。
        return detect_largest_color_blob(
            cv_image,
            target_color=self.target_color,
            min_area_pixels=self.min_area_pixels,
        )


def detection_to_message(detection: DetectionResult) -> TargetDetection:
    """把纯 Python 检测结果转换成 ROS 2 自定义消息。"""

    message = TargetDetection()
    message.label = detection.label
    message.confidence = detection.confidence
    message.center_x = detection.center_x
    message.center_y = detection.center_y
    message.width = detection.width
    message.height = detection.height
    message.is_tracking = detection.is_tracking
    return message


def main(args=None):
    rclpy.init(args=args)  # 初始化 ROS 2 Python 运行环境。
    node = ImageDetectorNode()  # 创建图像检测节点。
    try:
        rclpy.spin(node)  # 持续运行节点，等待 /camera/image_raw 回调。
    except KeyboardInterrupt:
        pass  # 用户 Ctrl-C 停止 launch 时，安静退出。
    finally:
        try:
            node.destroy_node()  # 销毁节点，释放 publisher/subscription 等 ROS 资源。
        except KeyboardInterrupt:
            pass  # 清理过程中再次收到 Ctrl-C 时，也保持干净退出。
        if rclpy.ok():
            rclpy.shutdown()  # 只有 context 还有效时才 shutdown，避免重复关闭。


if __name__ == "__main__":
    main()
