import unittest

import cv2
import numpy as np

from robot_perception.color_blob_detector import (
    DetectionResult,
    detect_largest_color_blob,
    draw_detection_box,
)


class ColorBlobDetectorTest(unittest.TestCase):
    """测试第 5 周第 1 小课的 OpenCV 颜色目标检测逻辑。"""

    def test_detects_largest_red_blob_with_normalized_box(self):
        image = np.zeros((100, 200, 3), dtype=np.uint8)
        image[20:80, 50:110] = (0, 0, 255)

        detection = detect_largest_color_blob(image, target_color="red", min_area_pixels=100)

        self.assertTrue(detection.is_tracking)
        self.assertEqual("red_target", detection.label)
        self.assertAlmostEqual(1.0, detection.confidence)
        self.assertAlmostEqual(0.4, detection.center_x, places=2)
        self.assertAlmostEqual(0.5, detection.center_y, places=2)
        self.assertAlmostEqual(0.3, detection.width, places=2)
        self.assertAlmostEqual(0.6, detection.height, places=2)

    def test_ignores_blob_smaller_than_minimum_area(self):
        image = np.zeros((100, 200, 3), dtype=np.uint8)
        image[10:20, 10:20] = (0, 0, 255)

        detection = detect_largest_color_blob(image, target_color="red", min_area_pixels=200)

        self.assertFalse(detection.is_tracking)
        self.assertEqual("", detection.label)
        self.assertEqual(0.0, detection.confidence)
        self.assertEqual(0.0, detection.center_x)
        self.assertEqual(0.0, detection.center_y)
        self.assertEqual(0.0, detection.width)
        self.assertEqual(0.0, detection.height)

    def test_detects_green_blob_with_green_label(self):
        image = np.zeros((100, 200, 3), dtype=np.uint8)
        image[30:70, 120:180] = (0, 255, 0)

        detection = detect_largest_color_blob(image, target_color="green", min_area_pixels=100)

        self.assertTrue(detection.is_tracking)
        self.assertEqual("green_target", detection.label)
        self.assertAlmostEqual(0.75, detection.center_x, places=2)
        self.assertAlmostEqual(0.5, detection.center_y, places=2)
        self.assertAlmostEqual(0.3, detection.width, places=2)
        self.assertAlmostEqual(0.4, detection.height, places=2)

    def test_draw_detection_box_keeps_image_shape_and_marks_box(self):
        image = np.zeros((100, 200, 3), dtype=np.uint8)
        detection = DetectionResult(
            label="red_target",
            confidence=1.0,
            center_x=0.4,
            center_y=0.5,
            width=0.3,
            height=0.6,
            is_tracking=True,
        )

        debug_image = draw_detection_box(image, detection)

        self.assertEqual(image.shape, debug_image.shape)
        self.assertFalse(np.array_equal(image, debug_image))
        self.assertTrue(np.any(cv2.inRange(debug_image, (0, 255, 255), (0, 255, 255))))


if __name__ == "__main__":
    unittest.main()
