import unittest

import numpy as np

from robot_perception.yolo_detector import YoloObjectDetector, detection_from_yolo_result


class FakeBoxes:
    def __init__(self, xyxy, conf, cls):
        self.xyxy = xyxy
        self.conf = conf
        self.cls = cls


class FakeResult:
    def __init__(self, xyxy, conf, cls, names):
        self.boxes = FakeBoxes(xyxy, conf, cls)
        self.names = names


class FakeModel:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def __call__(self, image, verbose=False):
        self.calls.append((image, verbose))
        return [self.result]


class YoloDetectorTest(unittest.TestCase):
    def test_converts_highest_confidence_box_to_normalized_detection(self):
        result = FakeResult(
            xyxy=[[10.0, 20.0, 50.0, 80.0], [100.0, 10.0, 180.0, 50.0]],
            conf=[0.40, 0.90],
            cls=[0.0, 1.0],
            names={0: "person", 1: "sports ball"},
        )

        detection = detection_from_yolo_result(
            result,
            image_shape=(100, 200, 3),
            confidence_threshold=0.25,
            target_class="",
        )

        self.assertTrue(detection.is_tracking)
        self.assertEqual("sports ball", detection.label)
        self.assertAlmostEqual(0.90, detection.confidence)
        self.assertAlmostEqual(0.70, detection.center_x, places=2)
        self.assertAlmostEqual(0.30, detection.center_y, places=2)
        self.assertAlmostEqual(0.40, detection.width, places=2)
        self.assertAlmostEqual(0.40, detection.height, places=2)

    def test_ignores_boxes_below_confidence_threshold(self):
        result = FakeResult(
            xyxy=[[10.0, 20.0, 50.0, 80.0]],
            conf=[0.20],
            cls=[0.0],
            names={0: "person"},
        )

        detection = detection_from_yolo_result(
            result,
            image_shape=(100, 200, 3),
            confidence_threshold=0.25,
            target_class="",
        )

        self.assertFalse(detection.is_tracking)
        self.assertEqual("", detection.label)

    def test_filters_by_target_class_name(self):
        result = FakeResult(
            xyxy=[[10.0, 20.0, 50.0, 80.0], [100.0, 10.0, 180.0, 50.0]],
            conf=[0.95, 0.90],
            cls=[0.0, 1.0],
            names={0: "person", 1: "sports ball"},
        )

        detection = detection_from_yolo_result(
            result,
            image_shape=(100, 200, 3),
            confidence_threshold=0.25,
            target_class="sports ball",
        )

        self.assertTrue(detection.is_tracking)
        self.assertEqual("sports ball", detection.label)
        self.assertAlmostEqual(0.90, detection.confidence)

    def test_detector_calls_injected_model_without_requiring_ultralytics(self):
        image = np.zeros((100, 200, 3), dtype=np.uint8)
        result = FakeResult(
            xyxy=[[10.0, 20.0, 50.0, 80.0]],
            conf=[0.80],
            cls=[0.0],
            names={0: "person"},
        )
        model = FakeModel(result)
        detector = YoloObjectDetector(
            model_path="unused.pt",
            confidence_threshold=0.25,
            target_class="person",
            model=model,
        )

        detection = detector.detect(image)

        self.assertTrue(detection.is_tracking)
        self.assertEqual("person", detection.label)
        self.assertEqual(1, len(model.calls))
        self.assertIs(image, model.calls[0][0])
        self.assertFalse(model.calls[0][1])


if __name__ == "__main__":
    unittest.main()
