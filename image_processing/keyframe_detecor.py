
import cv2
import numpy as np
import os

from matplotlib import pyplot as plt

class KeyFrameDetector:
    def __init__(self, frames_dir):
        frameItems = [frames_dir + "/" + file for file in os.listdir(frames_dir)]
        frameItems.sort()
        self.frames = frameItems

    def HBT(self):
          keyframes = []
          sumOfDiffs = []
          a =1

          if len(self.frames) == 1:
                return [self.frames[0]]

          for i in range(len(self.frames)):
            if i == len(self.frames) - 1:
                break
            current_frame = self.frames[i]
            next_frame = self.frames[i+1]

            current_img = cv2.cvtColor(cv2.imread(current_frame), cv2.COLOR_BGR2GRAY)
            current_img_hist = cv2.calcHist(current_img,[0,1,2],None,[8,8,8],[0,256,0,256,0,256])
            current_img_hist = cv2.normalize(current_img_hist, None).flatten()
            plt.plot(current_img_hist)

            next_img =  cv2.cvtColor(cv2.imread(next_frame), cv2.COLOR_BGR2GRAY)
            next_img_hist = cv2.calcHist(next_img,[0,1,2],None,[8,8,8],[0,256,0,256,0,256])
            next_img_hist = cv2.normalize(next_img_hist, None).flatten()
            plt.plot(next_img_hist)

            histogramDifference = cv2.compareHist(next_img_hist, current_img_hist, cv2.HISTCMP_INTERSECT)
            dict = {}
            dict["frame_filename"] = next_frame
            dict["SumOfDif"] = np.sum(histogramDifference)
            sumOfDiffs.append(dict)
            
          mean = np.mean([f["SumOfDif"] for f in sumOfDiffs])
          std = np.std([f["SumOfDif"] for f in sumOfDiffs])
          Threshold = std + (mean * a)

          keyframes = [f["frame_filename"] for f in sumOfDiffs if f["SumOfDif"] > Threshold]

          return keyframes

    def PBT(self):
            keyframes = []
            sumOfDiffs = []
            a = 1

            if len(self.frames) == 1:
                return [self.frames[0]]

            for i in range(len(self.frames)):
                if i == len(self.frames) - 1:
                    break
                current_frame = self.frames[i]
                next_frame = self.frames[i+1]

                current_img = cv2.cvtColor(cv2.imread(current_frame), cv2.COLOR_BGR2GRAY)
                next_img =  cv2.cvtColor(cv2.imread(next_frame), cv2.COLOR_BGR2GRAY)

                diff = cv2.absdiff(next_img, current_img)
                dict = {}
                dict["frame_filename"] = next_frame
                dict["SumOfDif"] = np.sum(diff)
                sumOfDiffs.append(dict)
            
            mean = np.mean([f["SumOfDif"] for f in sumOfDiffs])
            std = np.std([f["SumOfDif"] for f in sumOfDiffs])
            Threshold = std + (mean * a)

            keyframes = [f["frame_filename"] for f in sumOfDiffs if f["SumOfDif"] > Threshold]

            return keyframes
    
    def PixelDiff(self, threshold = 0.95):
            keyframes = []
            sumOfDiffs = []
            a = 1

            if len(self.frames) == 1:
                return [self.frames[0]]

            for i in range(len(self.frames)):
                if i == len(self.frames) - 1:
                    break
                current_frame = self.frames[i]
                next_frame = self.frames[i+1]

                current_img = cv2.cvtColor(cv2.imread(current_frame), cv2.COLOR_BGR2GRAY)
                next_img =  cv2.cvtColor(cv2.imread(next_frame), cv2.COLOR_BGR2GRAY)

                diff = cv2.absdiff(next_img, current_img)
                countOfNonZeros = np.count_nonzero(diff)
                frame_cal = (countOfNonZeros / (current_img.shape[0] * current_img.shape[1])) 
                if frame_cal >= threshold:
                     print(f"Comparing : {current_frame} {next_frame}: {frame_cal}")


if  __name__ == "__main__":
    detector = KeyFrameDetector("/app/edge_shared_files/esp32")
    print(detector.HBT())         
