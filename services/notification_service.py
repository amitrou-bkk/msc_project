
from src.services.event_triggered_service import (EventTriggeredService, NotificationData)

class NotificationService:
    def __init__(self) -> None:
        self.subscibers = []
        self.failedSubscribers = []

    def subsribe(self, topic: str, service : EventTriggeredService):
        self.subscibers.append({"topic": topic, "service": service})

    def notify(self, data:dict):
            topic = data["topic"]
            subscribers_to_notify = [sub for sub in self.subscibers if sub["topic"] == topic]
            for subscriber in subscribers_to_notify:
                 notification_data = NotificationData(data["content"])
                 success = subscriber["service"].OnNotified(notification_data)
                 if not success:
                      self.failedSubscribers.append(subscriber)
