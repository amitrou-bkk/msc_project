from edge_layer.edge_controller import EdgeController, IngressMode
from device_layer.CameraCapture import CameraCapture
from image_processing.feature_extraction import FeatureExtractor
from storage.FileStorage import FileStorage
from storage.AzureBlobStorage import AzureBlobSorage
import threading
import os
import sys

if __name__ == '__main__':
    try:
        arguments = sys.argv
        if arguments is not None and len(arguments) > 0:
            component = arguments[1]
            if component == "camera_controller":
                capture = CameraCapture(os.environ["CAMERA_IP"], os.environ["CAMERA_PORT"], False, os.environ["user"], os.environ["password"])
                image_capture_thread = threading.Thread(target = capture.Start)
                image_capture_thread.start()
            elif component == "edge":
                 edgeController = EdgeController(IngressMode.EdgeDataIngressMode.FileSystem)
                 edgeControllerThread = threading.Thread(target = edgeController.startListening)
                 edgeControllerThread.start()
            elif component == "feature_extractor":
                if os.environ["STORAGE_PROVIDER"] == "fs":
                    provider = FileStorage()
                elif os.environ["STORAGE_PROVIDER"] == "azure":
                    provider = AzureBlobSorage(os.environ["AZURE_STORAGE_ACCOUNT"], os.environ["AZURE_STORAGE_SAS_TOKEN"])
                else:
                  print("provider was not found")
                  exit()
                feature_extractor = FeatureExtractor(os.environ["INPUT_DATA"], provider)
                feature_extractor.ExtractFeatures()
            else:
                print("No module found!")
    except KeyboardInterrupt:
        image_capture_thread.join()
        edgeControllerThread.join()