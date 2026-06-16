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
        # 构造一张 100x200 的黑图，再手动画一个红色矩形。
        # OpenCV 使用 BGR 顺序，所以红色是 (0, 0, 255)，不是 RGB 的 (255, 0, 0)。
        image = np.zeros((100, 200, 3), dtype=np.uint8)
        image[20:80, 50:110] = (0, 0, 255)

        detection = detect_largest_color_blob(image, target_color="red", min_area_pixels=100)

        # 红框像素范围 x=50..109，y=20..79；归一化中心约为 (0.4, 0.5)。
        self.assertTrue(detection.is_tracking)
        self.assertEqual("red_target", detection.label)
        self.assertAlmostEqual(1.0, detection.confidence)
        self.assertAlmostEqual(0.4, detection.center_x, places=2)
        self.assertAlmostEqual(0.5, detection.center_y, places=2)
        self.assertAlmostEqual(0.3, detection.width, places=2)
        self.assertAlmostEqual(0.6, detection.height, places=2)

    def test_ignores_blob_smaller_than_minimum_area(self):
        # 这个红色小块只有 10x10 像素，面积小于阈值 200，应被当成噪声忽略。
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
        # 绿色圆柱对应的检测模式使用同一个算法，只是 HSV 阈值不同。
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
        # draw_detection_box 应该只添加可视化标记，不改变图像尺寸。
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
        # 黄色框的 BGR 值是 (0, 255, 255)，这里检查图像中确实出现过黄色像素。
        self.assertTrue(np.any(cv2.inRange(debug_image, (0, 255, 255), (0, 255, 255))))


if __name__ == "__main__":
    unittest.main()
