from src.services.event_triggered_service import EventTriggeredService, NotificationData
from src.storage.BaseStorage import BaseStorage
from utilities.file import (moveFile, getDirNameFromFile, fileOrDirectoryExists, createDirectory)
import os
import json

class ModelDownloadService(EventTriggeredService):
    def __init__(self, storageProvider: BaseStorage, saveFileLocation) -> None:
        self.modelSaveFileLocation = saveFileLocation
        self.storageProvider = storageProvider
        super().__init__()

    def Download(self, filePath):
        saved_file = self.storageProvider.read_file(filePath)
        if self.modelSaveFileLocation == None:
            self.modelSaveFileLocation = getDirNameFromFile(saved_file)

        if not fileOrDirectoryExists(self.modelSaveFileLocation):
            createDirectory(self.modelSaveFileLocation)
        print("Moving:" + os.path.join(self.modelSaveFileLocation, os.path.basename(saved_file)))
        moveFile(saved_file, os.path.join(self.modelSaveFileLocation, os.path.basename(saved_file)))

    def OnNotified(self, notification: NotificationData) -> bool:
        try :
            data = json.loads(notification.data)
            self.Download(data["file_url"])
            return True
        except Exception as ex:
            print(ex)
            return False