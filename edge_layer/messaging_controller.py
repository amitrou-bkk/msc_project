from src.messaging.messaging_service import MessagingService
from time import sleep
from src.services.notification_service import NotificationService
import uuid

class MessagingController:
    def __init__(self, messagingService : MessagingService, id: str, messageListeners: list) -> None:
        self.messagingService = messagingService
        self.controller_id = id
        self.failedMessages = []

        self.NotificationService = NotificationService()
        for messageListener in messageListeners:
            self.NotificationService.subsribe(messageListener.Topic, messageListener.NotifiableService)

    def startListening(self):
        while True:
            messages = self.messagingService.ReadMessage()
            for message in messages:
                temp_message = {"messageId": str(uuid.uuid4()), "content" : message.content, "topic": "new_trained_data"}
                self.NotificationService.notify(temp_message)
                if (len(self.NotificationService.failedSubscribers) == 0):
                    self.messagingService.DeleteMessage(message.id,  message.pop_receipt)
                else:
                    self.failedMessages.append(temp_message, self.NotificationService.failedSubscribers)
                sleep(5)
            
    