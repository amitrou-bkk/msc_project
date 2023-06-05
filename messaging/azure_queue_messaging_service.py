from src.messaging.messaging_service import MessagingService
from azure.storage.queue import QueueClient

class AzureMessagingService (MessagingService):
    def __init__(self, queueConnectionString, queueName) -> None:
        self.connectionstring = queueConnectionString
        self.queueName = queueName
        self.queue = QueueClient.from_connection_string(self.connectionstring, self.queueName)

    def ReadMessage(self):
        return self.queue.receive_messages()
    
    def DeleteMessage(self, message_id, pop_receipt=None):
        self.queue.delete_message(message_id, pop_receipt)

    def AddMessage(self, message:str):
        self.queue.send_message(message)
