import cv2
import numpy as np
import src.image_processing.utils as img_processing_utils

class SURF:

    LOWE_DESCRIPTOR_MATCH_RATIO = 0.75

    def __init__(self):
        pass

    def GenerateKeyPointsAndDescriptors(self, image):
       sourceImage = cv2.imread(image)

       grayscale = cv2.cvtColor(sourceImage, cv2.COLOR_BGR2GRAY) 

       surfObject = cv2.xfeatures2d.SURF_create()
       keypoints, descriptors = surfObject.detectAndCompute(grayscale, None)  

       return keypoints, descriptors

    def MatchImages(self, query_image, train_image, num_neighbours = 2):
        _ , query_descriptors = self.GenerateKeyPointsAndDescriptors(query_image)
        _ , train_descriptors = self.GenerateKeyPointsAndDescriptors(train_image)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(query_descriptors, train_descriptors, num_neighbours)

        good_matches = img_processing_utils.LowesRatioTest(matches, SURF.LOWE_DESCRIPTOR_MATCH_RATIO)
                       
        percent= ((len(good_matches))/len(train_descriptors)) * 100
        if percent >= 75.00:
            return True
        if percent < 75.00:
            return False

    def MatchDescriptors(self, query_descriptors, train_descriptors, num_neighbours = 2):
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(query_descriptors, train_descriptors, num_neighbours)

        good_matches = self.__LowesRatioTest(matches)

        percent= ((len(good_matches))/len(train_descriptors)) * 100
        if percent >= 75.00:
            return True
        if percent < 75.00:
            return False

    
