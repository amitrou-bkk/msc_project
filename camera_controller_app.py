from src.edge_layer.controllers.camera_controller import CameraController      
import os

def startCameraController():
     camera_controller = CameraController(os.environ.get("CAMERA_IP"), os.environ.get("CAMERA_PORT"), False, os.environ.get("CAMERA_USERNAME"), os.environ.get("CAMERA_PASSWORD"), os.environ.get("CAMERA_EXTRA_PATH"))
     if os.environ.get("ENABLE_CAMERA_STREAM_SIMULATION") is not None and os.environ.get("ENABLE_CAMERA_STREAM_SIMULATION").lower() == "true":
        print("Camera Simulation Started")
        camera_controller.StartSimulation()
     else:
        print("Real Camera Feed Started")
        camera_controller.Start()

if __name__ == '__main__':
    try:
       startCameraController()
    except KeyboardInterrupt:
        pass