from src.messaging.messaging_service import MessagingService
from time import sleep
from src.services.notification_service import NotificationService
import uuid
from src.storage.FileStorage import FileStorage
import src.utilities.string_utilities as utils
import json
import os

class MessagingController:
    POLL_INTERVAL = 5

    def __init__(self, messagingService : MessagingService, id: str, messageListeners: list) -> None:
        self.messagingService = messagingService
        self.controller_id = id
        self.failedMessages = []

        self.NotificationService = NotificationService()
        for messageListener in messageListeners:
            self.NotificationService.subsribe(messageListener.Topic, messageListener.NotifiableService)

    def startListening(self):
        print(f"Message Controller {self.controller_id} has started.")
        while True:
            print("Reading Messages from queue")
            messages = self.messagingService.ReadMessage()
            for message in messages:
                print(f"Found {message.id}")
                temp_message = {"messageId": str(uuid.uuid4()), "content" : message.content, "topic": "new_trained_data"}
                self.NotificationService.notify(temp_message)
                if (len(self.NotificationService.failedSubscribers) == 0):
                    self.messagingService.DeleteMessage(message.id,  message.pop_receipt)
                else:
                    self.failedMessages.append(self.NotificationService.failedSubscribers)
            sleep(5)

    def startScanInferenceResults(self, inference_results_dir_path, target_container_name):
        print("Started reading inference directory")
        if inference_results_dir_path == None or inference_results_dir_path == "":
            print("Inference directory not specified")
        file_storage = FileStorage()
       
        while True:
            files = file_storage.read_directory(inference_results_dir_path)
            for file in files:
                print(f"Found file {file}")
                notification_content = json.dumps({"file": file, "container": target_container_name})
                temp_message = {"messageId": str(uuid.uuid4()), "content" : notification_content, "topic": "new_data_to_cloud"}
                self.NotificationService.notify(temp_message)
                os.remove(file)
            


            
            
    