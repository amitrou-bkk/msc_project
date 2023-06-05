from src.services.event_triggered_service import EventTriggeredService, NotificationData
from src.storage.BaseStorage import BaseStorage
import json

class ModelDownloadService(EventTriggeredService):
    def __init__(self, storageProvider: BaseStorage) -> None:
        self.storageProvider = storageProvider
        super().__init__()

    def Download(self, filePath):
        self.storageProvider.read_file(filePath)

    def OnNotified(self, notification: NotificationData) -> bool:
        try :
            data = json.loads(notification.data)
            self.Download(data["file_url"])
            return True
        except Exception as ex:
            print(ex)
            return False