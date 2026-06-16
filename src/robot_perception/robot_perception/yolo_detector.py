from robot_perception.color_blob_detector import DetectionResult, empty_detection


class YoloDetectorDependencyError(RuntimeError):
    """选择 YOLO 后端但当前 Python 环境没有 ultralytics 时抛出。"""


def _as_list(value):
    if hasattr(value, "detach"):
        value = value.detach()
    if hasattr(value, "cpu"):
        value = value.cpu()
    if hasattr(value, "numpy"):
        value = value.numpy()
    if hasattr(value, "tolist"):
        return value.tolist()
    return list(value)


def _class_name(result, class_id: int) -> str:
    names = getattr(result, "names", {})
    if isinstance(names, dict):
        return names.get(class_id, str(class_id))
    if isinstance(names, (list, tuple)) and 0 <= class_id < len(names):
        return names[class_id]
    return str(class_id)


def detection_from_yolo_result(
    result,
    image_shape,
    confidence_threshold: float,
    target_class: str = "",
) -> DetectionResult:
    """把一帧 Ultralytics 检测结果转换成现有 DetectionResult。"""

    boxes = getattr(result, "boxes", None)
    if boxes is None:
        return empty_detection()

    xyxy_values = _as_list(boxes.xyxy)
    confidence_values = _as_list(boxes.conf)
    class_values = _as_list(boxes.cls)
    image_height, image_width = image_shape[:2]

    best_detection = empty_detection()
    best_confidence = confidence_threshold

    for xyxy, confidence, class_value in zip(xyxy_values, confidence_values, class_values):
        confidence = float(confidence)
        if confidence < best_confidence:
            continue

        class_id = int(class_value)
        label = _class_name(result, class_id)
        if target_class and label != target_class:
            continue

        x_min, y_min, x_max, y_max = [float(value) for value in xyxy]
        box_width = max(0.0, x_max - x_min)
        box_height = max(0.0, y_max - y_min)
        if box_width <= 0.0 or box_height <= 0.0:
            continue

        best_confidence = confidence
        best_detection = DetectionResult(
            label=label,
            confidence=confidence,
            center_x=((x_min + x_max) / 2.0) / image_width,
            center_y=((y_min + y_max) / 2.0) / image_height,
            width=box_width / image_width,
            height=box_height / image_height,
            is_tracking=True,
        )

    return best_detection


class YoloObjectDetector:
    """运行一个 Ultralytics YOLO 模型，并返回最优单目标检测。"""

    def __init__(
        self,
        model_path: str,
        confidence_threshold: float = 0.25,
        target_class: str = "",
        model=None,
    ):
        self.model = model if model is not None else self._load_model(model_path)
        self.confidence_threshold = confidence_threshold
        self.target_class = target_class

    def detect(self, image) -> DetectionResult:
        results = self.model(image, verbose=False)
        if not results:
            return empty_detection()

        return detection_from_yolo_result(
            results[0],
            image.shape,
            confidence_threshold=self.confidence_threshold,
            target_class=self.target_class,
        )

    def _load_model(self, model_path: str):
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise YoloDetectorDependencyError(
                "YOLO backend requires ultralytics. Activate the WSL YOLO environment "
                "or install it with: python3 -m pip install ultralytics"
            ) from exc

        return YOLO(model_path)
