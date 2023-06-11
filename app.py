from edge_layer.edge_controller import EdgeController, IngressMode
from device_layer.CameraCapture import CameraCapture
from image_processing.feature_extraction import FeatureExtractor
from messaging.message_listener import MessageListener
from services.model_download_service import ModelDownloadService
from messaging.azure_queue_messaging_service import AzureMessagingService
from edge_layer.messaging_controller import MessagingController
from src.edge_layer.inference_controller import InferenceController
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
            elif component == "inference_controller":
                 inference = InferenceController(os.environ.get("YOLO_MODEL"), os.environ.get("IMG_PREDICTION_REPO"),  os.environ.get("ML_MODEL_WEIGHTS_DIR"), None)
                 inference.start()
            elif component == "messaging_controller":
                    storage_provider = AzureBlobSorage(os.environ.get("AZURE_STORAGE_ACCOUNT"), os.environ.get("AZURE_STORAGE_SAS_TOKEN"))

                    modelDownloadService = ModelDownloadService(storage_provider, os.environ.get("ML_MODEL_WEIGHTS_DIR"))
                    message_listener_topic = "new_trained_data"
                    message_listener = MessageListener(message_listener_topic, modelDownloadService)

                    messagingService = AzureMessagingService(os.environ.get("AZ_QUEUE_CONSTR"), os.environ.get("AZ_QUEUE_NAME"))
                    msg_controller =  MessagingController(messagingService, "MessagingController1", [message_listener])
                    msg_controller.startListening()
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
        pass
        #captureThread.join()
        #edgeControllerThread.join()