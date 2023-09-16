import json
import os
import shutil
import src.edge_layer.ingression_models.ingression_mode as IngressMode
from src.edge_layer.ingression_models.ingress_factory import IngressFactory
from src.services.event_triggered_service import EventTriggeredService, NotificationData
import src.utilities.file as fileUtils
from time import sleep


class IngressImageService(EventTriggeredService):
    def __init__(self):
        self.inference_dir = "/app/edge_shared_files/image_inference"
        self.allowedExtensions = [".jpg",".tiff", ".jpeg", ".img"]
        super().__init__()

    def StageFileForInference(self, img):
       print(f"Start Staging of {img}")
       if (not os.path.exists(self.inference_dir)):
            os.mkdir(self.inference_dir)

       file_name, file_extension = fileUtils.get_filename_and_extension(img)

       if (file_extension not in self.allowedExtensions):
            return
       
       staged_file = os.path.join(self.inference_dir, os.path.basename(file_name) + file_extension)
       shutil.move(img, staged_file)
       print(f"Staged to Staging of {staged_file}")

    def OnNotified(self, notification: NotificationData) -> bool:
        try :
            data = json.loads(notification.data)
            self.StageFileForInference(data["file"])
            return True
        except Exception as ex:
            print(ex)
            return False