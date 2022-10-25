from edge_layer.edge_controller import EdgeController, IngressMode
from device_layer.CameraCapture import CameraCapture
from image_processing.feature_extraction import FeatureExtractor
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
                feature_extractor = FeatureExtractor("test")
                feature_extractor.ExtractFeatures()
            else:
                print("No module found!")
    except KeyboardInterrupt:
        image_capture_thread.join()
        edgeControllerThread.join()