import unittest
import os
import src.utilities.file as fileUtils
from src.image_processing.SIFT import SIFT

class SIFT_TEST (unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.test_image="/home/amitrou/msc_project/src/tests/img_test.jpg"
        self.processor = SIFT()

    def test_keypoints_are_extracted(self):        
        keypoints, _ = self.processor.GenerateKeyPointsAndDescriptors(self.test_image)
        self.assertIsNotNone(keypoints)

    def test_descriptors_are_extracted(self):
        _, descriptors = self.processor.GenerateKeyPointsAndDescriptors(self.test_image)
        self.assertIsNotNone(descriptors)

    def test_descriptors_are_saved_correctly(self):
        _, descriptors = self.processor.GenerateKeyPointsAndDescriptors(self.test_image)
        fileUtils.save_array_to_file(descriptors, "test.npy")
        self.assertTrue(os.path.exists("test.npy"))

    def test_descriptors_are_loaded_correctly(self):
        _, descriptors = self.processor.GenerateKeyPointsAndDescriptors(self.test_image)
        fileUtils.save_array_to_file(descriptors, "test.npy")
       
        arr = fileUtils.load_file_to_array("test.npy")
        self.assertTrue(arr is not None)

if __name__ == '__main__':
    unittest.main()