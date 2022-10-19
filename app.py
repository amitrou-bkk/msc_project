from edge_layer.edge_controller import EdgeController, IngressMode
from device_layer.CameraCapture import CameraCapture
import threading
import os

if __name__ == '__main__':
    try:
        capture = CameraCapture(os.environ["CAMERA_IP"], os.environ["CAMERA_PORT"], False, os.environ["user"], os.environ["password"])
        image_capture_thread = threading.Thread(target = capture.Start)
        image_capture_thread.start()
        
        edgeController = EdgeController(IngressMode.EdgeDataIngressMode.FileSystem)
        edgeControllerThread = threading.Thread(target = edgeController.startListening)
        edgeControllerThread.start()
        
    except KeyboardInterrupt:
        image_capture_thread.join()
        edgeControllerThread.join()