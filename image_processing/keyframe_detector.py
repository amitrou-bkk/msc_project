
import cv2
import numpy as np
import os
import re
from matplotlib import pyplot as plt

class KeyFrameDetector:
    def __init__(self):
        self.algorithms = ["PBT", "HBT"]

    def ExtractFromDirectory(self, frames_dir, algorithm = "PBT"):
       
        selectedAlgorithm = self.algorithms[self.algorithms.index(algorithm)]
        frameItems = [frames_dir + "/" + file for file in os.listdir(frames_dir)]
        frameItems.sort(key=lambda f: int(re.sub('\D', '', f)))
        frames = frameItems
        keyframes = []
        a = 1

        if len(frames) == 1:
            return [frames[0]]
        
        for i in range(0, len(frames)):
            if i == 0:
                 keyframes.append(frames[i])
                 continue
            
            previous_frame = frames[i-1]
            current_frame = frames[i]
            result = False

            if selectedAlgorithm == "HBT":
                result = self.HBT(previous_frame, current_frame)
            elif selectedAlgorithm == "PBT":
                 result = self.PBT(previous_frame, current_frame)
            else:
                 result = False
            
            if result:
                 keyframes.append(current_frame)

        return keyframes
    
    def PBT(self, previous_frame_image, current_frame_image, threshold = 0.5):
        prv_img = cv2.cvtColor(cv2.imread(previous_frame_image), cv2.COLOR_BGR2GRAY)
        curr_img =  cv2.cvtColor(cv2.imread(current_frame_image), cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(curr_img, prv_img)
        countOfNonZeros = np.count_nonzero(diff)
        proportional_pixel_diff = (countOfNonZeros / (curr_img.shape[0] * curr_img.shape[1]))
        return proportional_pixel_diff > threshold

    def HBT(self, previous_frame_image, current_frame_image):
        prv_img = cv2.imread(previous_frame_image, cv2.IMREAD_GRAYSCALE)
        prv_img_hist = cv2.calcHist([prv_img], [0], None, [8], [0, 256])
        prv_img_hist = cv2.normalize(prv_img_hist, None).flatten()
        #plt.plot(current_img_hist)

        curr_img =  cv2.imread(current_frame_image, cv2.IMREAD_GRAYSCALE)
        curr_img_hist = cv2.calcHist([curr_img], [0], None, [8],[0, 256])
        curr_img_hist = cv2.normalize(curr_img_hist, None).flatten()

        abs_frame_difference = cv2.absdiff(current_frame_image, previous_frame_image) 
        mean = np.mean(abs_frame_difference)
        std = np.std(abs_frame_difference)
        th =  std + (mean * 1)
        #plt.plot(next_img_hist)

        histogramDifference = cv2.compareHist(curr_img_hist, prv_img, cv2.HISTCMP_INTERSECT)
        # histogramSimilarity = cv2.compareHist(next_img_hist, current_img_hist, cv2.HISTCMP_CORREL)
        
        print(f"Keyframe: Th:{th} HDiff: {histogramDifference} Correl:{histogramDifference} {current_frame_image}")

        return histogramDifference > th
    
    def Stats(self, listItems):
         print(f'''
         Print Stats:
         NoItems:{len(listItems)}
         Mean:{np.mean(listItems)}
         Std:{np.std(listItems)}
         Max:{np.max(listItems)}
         Min:{np.min(listItems)}
         ''')

    def Histogram(self, list,bins=10):
         max_value = np.max(list)
         min_value = np.min(list)
         bin_range = (max_value-min_value) / bins

         data = np.array(list)
         bin_values=[]
         last_bin_value = 0
         for i in range(bins):
              bin_values.append(last_bin_value)
              last_bin_value = last_bin_value + bin_range
        
         plt.hist(data, bin_values) 
         plt.title("histogram") 
         plt.show()
   
def ExtractFramesFromVideo(video_path, out_dir):
    if not os.path.exists(out_dir):
         os.makedirs(out_dir)
    
    vidcap = cv2.VideoCapture(video_path)
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(os.path.join(out_dir, "frame%d.jpg" % count), image)     # save frame as JPEG file      
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1

if  __name__ == "__main__":
    detector = KeyFrameDetector("/home/amitrou/msc_project/src/test_face_mask_images/movie_extracted_frames")
    detector.ExtractFromDirectory("/home/amitrou/msc_project/src/test_face_mask_images/movie_extracted_frames", "HBT")
    #ffmpeg command ffmpeg -skip_frame nokey -i mov1.mp4 -vsync vfr -frame_pts true out-%02d.jpeg      