
from src.edge_layer.messaging_controller import MessagingController
from src.messaging.azure_queue_messaging_service import AzureMessagingService
from src.messaging.message_listener import MessageListener
from src.services.model_download_service import ModelDownloadService
from src.storage.AzureBlobStorage import AzureBlobSorage
import config

storage_provider = AzureBlobSorage(config.blob_storage_account, config.blob_storage_sas_token)
message_listener = MessageListener("new_trained_data", ModelDownloadService(storage_provider, "/app/edge_shared_files/ml_model_weights"))

messagingService = AzureMessagingService(config.connectionString, config.queueName)
msg_controller =  MessagingController(messagingService, "MessagingController1", [message_listener])
msg_controller.startListening()
