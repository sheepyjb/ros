from dataclasses import dataclass

import cv2


@dataclass(frozen=True)
class DetectionResult:
    label: str
    confidence: float
    center_x: float
    center_y: float
    width: float
    height: float
    is_tracking: bool


def empty_detection() -> DetectionResult:
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
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    if target_color == "red":
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
        return cv2.inRange(hsv_image, (40, 60, 60), (85, 255, 255))

    raise ValueError(f"Unsupported target color: {target_color}")


def detect_largest_color_blob(
    image,
    target_color: str = "red",
    min_area_pixels: float = 200.0,
) -> DetectionResult:
    mask = _build_color_mask(image, target_color)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return empty_detection()

    largest_contour = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_contour)
    if area < min_area_pixels:
        return empty_detection()

    x, y, width, height = cv2.boundingRect(largest_contour)
    image_height, image_width = image.shape[:2]

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
    debug_image = image.copy()
    if not detection.is_tracking:
        return debug_image

    image_height, image_width = debug_image.shape[:2]
    box_width = int(detection.width * image_width)
    box_height = int(detection.height * image_height)
    center_x = int(detection.center_x * image_width)
    center_y = int(detection.center_y * image_height)
    left = max(0, center_x - box_width // 2)
    top = max(0, center_y - box_height // 2)
    right = min(image_width - 1, left + box_width)
    bottom = min(image_height - 1, top + box_height)

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
