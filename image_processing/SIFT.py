import cv2
import numpy as np
class SIFT:
    def __init__(self):
        pass

    def GenerateKeyPointsAndDescriptors(self, image):
       sourceImage = cv2.imread(image)

       grayscale = cv2.cvtColor(sourceImage, cv2.COLOR_BGR2GRAY) 

       siftObject = cv2.xfeatures2d.SIFT_create()
       keypoints, descriptors = siftObject.detectAndCompute(grayscale, None)  

       return keypoints, descriptors

    def MatchImages(self, query_image, train_image, num_neighbours = 2):
        _ , query_descriptors = self.GenerateKeyPointsAndDescriptors(query_image)
        _ , train_descriptors = self.GenerateKeyPointsAndDescriptors(train_image)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(query_descriptors, train_descriptors, num_neighbours)
        good_matches = []
        for m,n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
                a=len(good_matches)
                percent=(a*100)/len(train_descriptors)
                if percent >= 75.00:
                    return True
                if percent < 75.00:
                    return False

    def MatchDescriptors(self, query_descriptors, train_descriptors, num_neighbours = 2):
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(query_descriptors, train_descriptors, num_neighbours)
        good_matches = []
        for m,n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
                a=len(good_matches)
                percent=(a*100)/len(train_descriptors)
                if percent >= 75.00:
                    return True
                if percent < 75.00:
                    return False