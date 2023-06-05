from abc import ABC, abstractmethod
class MessagingService(ABC):

    @abstractmethod
    def ReadMessage(self):
        pass
    
    @abstractmethod
    def DeleteMessage(self, message_id, pop_receipt = None):
        pass