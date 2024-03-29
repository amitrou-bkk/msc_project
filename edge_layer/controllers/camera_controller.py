import cv2
import time
import os
import imageio.v3 as iio
import requests
from datetime import datetime
from utilities.file import copyfile

class CameraController:
    def __init__(self, camera_ip, camera_port = None , isHttps = False, user = None, password = None, camera_stream_path = None):
        self.url = "https://" if isHttps else "http://"
        self.url += f"{user}:{password}@" if user is not None and password is not None else ""
        self.url += camera_ip
        self.url += f":{camera_port}" if camera_port is not None else ""
        self.url += f"/{camera_stream_path}"
        self.IsCapturing = False
       
    def Start(self, delayInSeconds=1):
        cap = cv2.VideoCapture(self.url)
        self.IsCapturing = True
        
        if not os.path.exists(os.path.join("/app/edge_shared_files", os.environ["CAMERA_ID"])):
            os.makedirs(os.path.join("/app/edge_shared_files", os.environ["CAMERA_ID"]))
        
        while (self.IsCapturing):
            current_date = datetime.now()
            dateStr =  current_date.strftime('%Y%m%d%H%M%S')
            print("Reading frame")
            _, frame = cap.read()
            #cv2.imshow("Frame", frame)
            frame_img_name = os.path.join("/app/edge_shared_files/", os.environ["CAMERA_ID"] + "/",  dateStr + ".jpg")
            try:
                iio.imwrite(frame_img_name, frame)
            except:
                print("Error Saving the Captured image")

            if cv2.waitKey(1) == ord('q'):
                break
            time.sleep(delayInSeconds)

        cap.release()
        cv2.destroyAllWindows()

    def Stop(self):
        self.IsCapturing = False

    def StartSimulation(self, delayInSeconds=5):
        self.IsCapturing = True
        sample_images_path = os.path.join(os.path.abspath(os.path.join(__file__ ,"../../..")), "camera_simulation_images")
        print(sample_images_path)
        if not os.path.exists(os.path.join("/app/edge_shared_files", os.environ["CAMERA_ID"])):
            os.makedirs(os.path.join("/app/edge_shared_files", os.environ["CAMERA_ID"]))

        while (self.IsCapturing):
            sample_files = os.listdir(sample_images_path)
            for sample_file in sample_files:
                current_date = datetime.now()
                dateStr = current_date.strftime('%Y%m%d%H%M%S')
                image_created = os.path.join("/app/edge_shared_files/", os.environ["CAMERA_ID"] + "/",  dateStr + ".jpg")
                copyfile(os.path.join(sample_images_path, sample_file), image_created)
                print(f"Dummy image {image_created} saved.")
                time.sleep(1)

            time.sleep(delayInSeconds)

    def __set_resolution(self, url: str, index: int=1, verbose: bool=False):
        try:
            if verbose:
                resolutions = "10: UXGA(1600x1200)\n9: SXGA(1280x1024)\n8: XGA(1024x768)\n7: SVGA(800x600)\n6: VGA(640x480)\n5: CIF(400x296)\n4: QVGA(320x240)\n3: HQVGA(240x176)\n0: QQVGA(160x120)"
                print("available resolutions\n{}".format(resolutions))

            if index in [10, 9, 8, 7, 6, 5, 4, 3, 0]:
                requests.get(url + "/control?var=framesize&val={}".format(index))
            else:
                print("Wrong index")
        except:
            print("SET_RESOLUTION: something went wrong")