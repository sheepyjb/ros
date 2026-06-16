import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from robot_interfaces.msg import TargetDetection
from sensor_msgs.msg import Image

from robot_perception.color_blob_detector import (
    DetectionResult,
    detect_largest_color_blob,
    draw_detection_box,
)


class ImageDetectorNode(Node):
    def __init__(self):
        super().__init__("image_detector_node")

        self.declare_parameter("image_topic", "/camera/image_raw")
        self.declare_parameter("detection_topic", "/target_detection")
        self.declare_parameter("debug_image_topic", "/target_detection/debug_image")
        self.declare_parameter("target_color", "red")
        self.declare_parameter("min_area_pixels", 200.0)
        self.declare_parameter("publish_debug_image", True)

        self.target_color = self.get_parameter("target_color").value
        self.min_area_pixels = float(self.get_parameter("min_area_pixels").value)
        self.publish_debug_image = bool(self.get_parameter("publish_debug_image").value)

        image_topic = self.get_parameter("image_topic").value
        detection_topic = self.get_parameter("detection_topic").value
        debug_image_topic = self.get_parameter("debug_image_topic").value

        self.bridge = CvBridge()
        self.detection_publisher = self.create_publisher(TargetDetection, detection_topic, 10)
        self.debug_image_publisher = self.create_publisher(Image, debug_image_topic, 10)
        self.image_subscription = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            qos_profile_sensor_data,
        )

    def image_callback(self, image_msg: Image) -> None:
        try:
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, desired_encoding="bgr8")
        except Exception as exc:
            self.get_logger().warning(f"无法把 ROS Image 转成 OpenCV 图像：{exc}")
            return

        detection = detect_largest_color_blob(
            cv_image,
            target_color=self.target_color,
            min_area_pixels=self.min_area_pixels,
        )
        self.detection_publisher.publish(detection_to_message(detection))

        if not self.publish_debug_image:
            return

        debug_image = draw_detection_box(cv_image, detection)
        debug_msg = self.bridge.cv2_to_imgmsg(debug_image, encoding="bgr8")
        debug_msg.header = image_msg.header
        self.debug_image_publisher.publish(debug_msg)


def detection_to_message(detection: DetectionResult) -> TargetDetection:
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
    rclpy.init(args=args)
    node = ImageDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            node.destroy_node()
        except KeyboardInterrupt:
            pass
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
