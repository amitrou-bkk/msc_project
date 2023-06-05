from src.messaging.azure_queue_messaging_service import AzureMessagingService
import json
from time import sleep
import datetime
import config

def generate_file_name(base_filename):
    now = datetime.datetime.now() # current date and time
    return  now.strftime("%Y%m%dT%H%M%S") + "_" + base_filename

messagingService = AzureMessagingService(config.connectionString, config.queueName)

while True:
    message =  {
        "file_url": "yoloweights:20230521110311-best.pt"
    }

    messagingService.AddMessage(json.dumps(message))
    print(f"Sent {message}")
    sleep(10)