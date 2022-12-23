# Using Android IP Webcam video .jpg stream (tested) in Python2 OpenCV3
import cv2
import numpy as np
import time
import os
import imageio.v3 as iio
from datetime import datetime
from PIL import Image


class CameraCapture:

    def __init__(self, camera_ip, camera_port = None , isHttps = False, user = None, password = None):
        self.url = "https://" if isHttps else "http://"
        self.url += f"{user}:{password}@" if user is not None and password is not None else ""
        self.url += camera_ip
        self.url += f":{camera_port}" if camera_port is not None else ""
        self.url += "/video"
        self.IsCapturing = False
       
    def Start(self, delayInSeconds=0):
        cap = cv2.VideoCapture(self.url)
        frame_count = delayInSeconds
        self.IsCapturing = True
        
        if not os.path.exists(os.path.join("/app/edge_shared_files", os.environ["CAMERA_ID"])):
            os.makedirs(os.path.join("/app/edge_shared_files", os.environ["CAMERA_ID"]))

        while (self.IsCapturing):
            current_date = datetime.now()
            dateStr =  current_date.strftime('%Y%m%d%H%M%S')
           
            _, frame = cap.read()
            cv2.imshow("Frame", frame)
            frame_img_name = os.path.join("/app/edge_shared_files/", os.environ["CAMERA_ID"] + "/",  dateStr + ".jpg")
            iio.imwrite(frame_img_name, frame)
           
            frame_count = frame_count + 1

            if cv2.waitKey(1) == ord('q'):
                break
            time.sleep(delayInSeconds)

        cap.release()
        cv2.destroyAllWindows()

    def Stop(self):
        self.IsCapturing = False

    def StartSimulation(self, delayInSeconds=5):
       
        frame_count = 0
        self.IsCapturing = True
        
        if not os.path.exists(os.path.join("/app/edge_shared_files", os.environ["CAMERA_ID"])):
            os.makedirs(os.path.join("/app/edge_shared_files", os.environ["CAMERA_ID"]))

        while (self.IsCapturing):
            current_date = datetime.now()
            dateStr = current_date.strftime('%Y%m%d%H%M%S')
           
            image = Image.new("RGB", (300, 300))
            image_created = os.path.join("/app/edge_shared_files/", os.environ["CAMERA_ID"] + "/",  dateStr + ".jpg")
            image.save(image_created, 'JPEG')
            print(f"Dummy image {image_created} saved.")
            frame_count += 1

            if frame_count >= 5:
                self.IsCapturing = False

            time.sleep(delayInSeconds)

    def RandomImage(a):
        image = Image.new("RGB", (300, 300))
        image.save("blank.jpg") 