from abc import ABC, abstractmethod
class NotificationData:
    def __init__(self, data: str) -> None:
       self.data = data

class EventTriggeredService(ABC):
    def __init__(self) -> None:
        self.failedNotifications = []
        super().__init__()  
    @abstractmethod
    def OnNotified(self, data: NotificationData) -> bool:
        pass
