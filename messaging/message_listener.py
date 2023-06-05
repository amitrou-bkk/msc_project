from src.services.event_triggered_service import EventTriggeredService


class MessageListener:
    def __init__(self, topic: str, notifiable_service : EventTriggeredService) -> None:
        self.Topic = topic
        self.NotifiableService = notifiable_service