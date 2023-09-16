from src.edge_layer.controllers.ingestion_controller import IngestionController
from src.edge_layer.controllers.camera_controller import CameraController      
from messaging.message_listener import MessageListener
from services.model_download_service import ModelDownloadService
from messaging.azure_queue_messaging_service import AzureMessagingService
from edge_layer.controllers.messaging_controller import MessagingController
from src.edge_layer.controllers.inference_controller import InferenceController
from src.services.cloud_upload_service import CloudUploadBlobService
from src.services.ingress_image_service import IngressImageService
from storage.AzureBlobStorage import AzureBlobStorage
import threading
import os
import sys

if __name__ == '__main__':
    try:
        arguments = sys.argv
        if arguments is not None and len(arguments) > 1:
            component = arguments[1]
            if component == "camera_controller":
                capture = CameraController(os.environ.get("CAMERA_IP"), os.environ.get("CAMERA_PORT"), False, os.environ.get("CAMERA_USERNAME"), os.environ.get("CAMERA_PASSWORD"), os.environ.get("CAMERA_EXTRA_PATH"))
                if os.environ.get("ENABLE_CAMERA_STREAM_SIMULATION") is not None and os.environ.get("ENABLE_CAMERA_STREAM_SIMULATION").lower() == "true":
                    print("Camera Simulation Started")
                    captureThread = threading.Thread(target = capture.StartSimulation)
                else:
                    print("Real Camera Feed Started")
                    captureThread = threading.Thread(target = capture.Start)
                captureThread.start()
            elif component == "ingest_controller":
                 ingestionController = IngestionController()
                 ingestionController.start()
            elif component == "inference_controller":
                 inference = InferenceController(os.environ.get("YOLO_MODEL"), os.environ.get("IMG_PREDICTION_REPO"),  os.environ.get("ML_MODEL_WEIGHTS_DIR"), os.environ.get("ML_MODEL_RESULTS_DIR"))
                 inference.start()
            elif component == "messaging_controller":
                    message_listeners = []

                    # Azure Queue registration message listener
                    storage_provider = AzureBlobStorage(os.environ.get("AZURE_STORAGE_ACCOUNT"), os.environ.get("AZURE_STORAGE_SAS_TOKEN"))
                    modelDownloadService = ModelDownloadService(storage_provider, os.environ.get("ML_MODEL_WEIGHTS_DIR"))
                    message_listener_topic_download_service = "new_trained_data"
                    message_listener_download_service = MessageListener(message_listener_topic_download_service, modelDownloadService)
                    messagingService = AzureMessagingService(os.environ.get("AZ_QUEUE_CONSTR"), os.environ.get("AZ_QUEUE_NAME"))
                    message_listeners.append(message_listener_download_service)

                    # InferenceResults registration message listener
                    
                    cloud_upload_service = CloudUploadBlobService(os.environ.get("AZURE_STORAGE_ACCOUNT"), os.environ.get("AZURE_INF_RESULTS_STORAGE_SAS_TOKEN"))
                    message_listener_topic_cloud_upload_service = "new_data_to_cloud"
                    message_listener_cloud_upload_service = MessageListener(message_listener_topic_cloud_upload_service, cloud_upload_service)
                    message_listeners.append(message_listener_cloud_upload_service)

                    image_ingress_service = IngressImageService()
                    #IngressImageService registration message listener

                    image_ingress_service = IngressImageService()
                    message_listener_topic_image_ingress_service = "new_image_received"
                    message_listener_image_ingress_service = MessageListener(message_listener_topic_image_ingress_service, image_ingress_service)
                    message_listeners.append(message_listener_image_ingress_service)

                    msg_controller =  MessagingController(messagingService, "MessagingController1", message_listeners)
                    cloudMessagesListenerThread = threading.Thread(target = msg_controller.startListeningToTrainModelChanges)
                    edgeMessageInferenceListenerThread = threading.Thread(target= msg_controller.startListeningToNewInferenceData, args = (os.environ.get("ML_MODEL_RESULTS_DIR"), os.environ.get("ML_MODEL_RESULTS_CONTAINER"),))
                    edgeCapturedImageIngestionListenerThread = threading.Thread(target= msg_controller.startListeningToReadyImagesForInference, args = (os.environ.get("INCOMING_IMG_REPO"),))
                    
                    cloudMessagesListenerThread.start()
                    edgeMessageInferenceListenerThread.start()
                    edgeCapturedImageIngestionListenerThread.start()
            else:
                print("No module found!")
    except KeyboardInterrupt:
        pass
        #captureThread.join()
        #edgeControllerThread.join()