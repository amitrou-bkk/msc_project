from src.messaging.messaging_service import MessagingService
from time import sleep
from src.services.notification_service import NotificationService
import uuid
import src.utilities.string_utilities as utils

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
            
    