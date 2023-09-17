from src.edge_layer.controllers.ingestion_controller import IngestionController    

def startIngestController():
    ingestionController = IngestionController()
    ingestionController.start()

if __name__ == '__main__':
    try:
       startIngestController()
    except KeyboardInterrupt:
        pass