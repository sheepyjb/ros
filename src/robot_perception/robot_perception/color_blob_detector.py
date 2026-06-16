from dataclasses import dataclass

import cv2  # OpenCV 图像处理库，本课用它做颜色阈值、轮廓查找和画框。


@dataclass(frozen=True)
class DetectionResult:
    """纯 Python 检测结果，字段和 robot_interfaces/msg/TargetDetection 对齐。"""

    label: str  # 目标类别名称，例如 red_target 或 green_target。
    confidence: float  # 检测置信度；颜色检测没有模型概率，本课检测到就给 1.0。
    center_x: float  # 检测框中心 x，使用 0.0 到 1.0 的归一化坐标。
    center_y: float  # 检测框中心 y，使用 0.0 到 1.0 的归一化坐标。
    width: float  # 检测框宽度，占整张图像宽度的比例。
    height: float  # 检测框高度，占整张图像高度的比例。
    is_tracking: bool  # 是否检测到足够大的目标。


def empty_detection() -> DetectionResult:
    """生成“没有检测到目标”的统一返回值。"""

    return DetectionResult(
        label="",
        confidence=0.0,
        center_x=0.0,
        center_y=0.0,
        width=0.0,
        height=0.0,
        is_tracking=False,
    )


def _build_color_mask(image, target_color: str):
    """把 BGR 图像转成二值 mask，白色区域表示目标颜色。"""

    # cv_bridge 输出的是 OpenCV 常用 BGR 顺序，不是 RGB。
    # HSV 比 BGR 更适合做颜色阈值：H 表示色相，S 表示饱和度，V 表示亮度。
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    if target_color == "red":
        # 红色在 HSV 的色相环上跨越 0 度，所以要分成两段：
        # 一段靠近 0，一段靠近 179，然后把两个 mask 合并。
        lower_red_1 = (0, 80, 80)
        upper_red_1 = (10, 255, 255)
        lower_red_2 = (170, 80, 80)
        upper_red_2 = (179, 255, 255)
        return cv2.inRange(hsv_image, lower_red_1, upper_red_1) | cv2.inRange(
            hsv_image,
            lower_red_2,
            upper_red_2,
        )

    if target_color == "green":
        # Gazebo 里的绿色圆柱大致落在 40 到 85 的 Hue 范围。
        return cv2.inRange(hsv_image, (40, 60, 60), (85, 255, 255))

    raise ValueError(f"Unsupported target color: {target_color}")


def detect_largest_color_blob(
    image,
    target_color: str = "red",
    min_area_pixels: float = 200.0,
) -> DetectionResult:
    """检测图像中最大的指定颜色区域，并返回归一化检测框。"""

    mask = _build_color_mask(image, target_color)

    # 开运算会先腐蚀再膨胀，可以去掉零散噪点，避免小亮点被误认为目标。
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # contour 可以理解为二值 mask 中每块白色连通区域的外轮廓。
    # RETR_EXTERNAL 只取最外层轮廓，本课不关心目标内部孔洞。
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return empty_detection()

    # 如果画面里有多个同色区域，先选面积最大的那个，后续 YOLO 课再讨论多目标。
    largest_contour = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_contour)
    if area < min_area_pixels:
        # 面积太小通常是噪声或远处小点，不作为有效跟踪目标。
        return empty_detection()

    # boundingRect 返回像素坐标：左上角 x/y 和框的 width/height。
    x, y, width, height = cv2.boundingRect(largest_contour)
    image_height, image_width = image.shape[:2]

    # 这里转成归一化坐标，后续控制节点就不需要知道图像分辨率。
    return DetectionResult(
        label=f"{target_color}_target",
        confidence=1.0,
        center_x=(x + width / 2.0) / image_width,
        center_y=(y + height / 2.0) / image_height,
        width=width / image_width,
        height=height / image_height,
        is_tracking=True,
    )


def draw_detection_box(image, detection: DetectionResult):
    """在图像副本上画检测框，用于发布 debug image 给 RViz2 观察。"""

    # 不直接修改原图，避免调试图像影响后续算法处理。
    debug_image = image.copy()
    if not detection.is_tracking:
        return debug_image

    image_height, image_width = debug_image.shape[:2]

    # DetectionResult 里保存的是归一化坐标，画图前要换回像素坐标。
    box_width = int(detection.width * image_width)
    box_height = int(detection.height * image_height)
    center_x = int(detection.center_x * image_width)
    center_y = int(detection.center_y * image_height)
    left = max(0, center_x - box_width // 2)
    top = max(0, center_y - box_height // 2)
    right = min(image_width - 1, left + box_width)
    bottom = min(image_height - 1, top + box_height)

    # OpenCV 的颜色仍然是 BGR；(0, 255, 255) 是黄色。
    color = (0, 255, 255)
    cv2.rectangle(debug_image, (left, top), (right, bottom), color, 2)
    cv2.putText(
        debug_image,
        detection.label,
        (left, max(15, top - 8)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        1,
        cv2.LINE_AA,
    )
    return debug_image
