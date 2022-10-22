import unittest
import os
from src.image_processing.SIFT import SIFT
class SIFT_TEST (unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.test_image="/home/amitrou/msc_project/src/tests/img_test.jpg"

    def test_keypoints_are_extracted(self):
        sift_processor = SIFT()
        results=sift_processor.GenerateKeyPointsAndDescriptors(self.test_image)
        self.assertSetEqual(1,1)

if __name__ == '__main__':
    unittest.main()