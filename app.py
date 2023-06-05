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
        if arguments is not None and len(arguments) > 1:
            component = arguments[1]
            if component == "camera_controller":
                capture = CameraCapture(os.environ.get("CAMERA_IP"), os.environ.get("CAMERA_PORT"), False, os.environ.get("CAMERA_USERNAME"), os.environ.get("CAMERA_PASSWORD"), os.environ.get("CAMERA_EXTRA_PATH"))
                if os.environ.get("ENABLE_CAMERA_STREAM_SIMULATION") is not None and os.environ.get("ENABLE_CAMERA_STREAM_SIMULATION").lower() == "true":
                    print("Camera Simulation Started")
                    captureThread = threading.Thread(target = capture.StartSimulation)
                else:
                    print("Real Camera Feed Started")
                    captureThread = threading.Thread(target = capture.Start)
                captureThread.start()
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
                  print("Storage Provider was not found")
                  exit()
                
                feature_extractor = FeatureExtractor(os.environ["INPUT_DATA"], provider)
                if os.environ["RUN_MODE"] == None or os.environ["RUN_MODE"] == ""  or os.environ["RUN_MODE"] == "CONTINUOUS":
                    extractorThread = threading.Thread(target = feature_extractor.ExtractFeatures, args = [True])
                    extractorThread.start()
                elif os.environ["RUN_MODE"].lower() ==  "on_demand":
                    feature_extractor.ExtractFeatures()
            else:
                print("No module found!")
    except KeyboardInterrupt:
        captureThread.join()
        edgeControllerThread.join()