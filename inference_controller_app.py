from src.edge_layer.controllers.inference_controller import InferenceController
import os

def startInferenceController():
     inference = InferenceController(os.environ.get("YOLO_MODEL"), os.environ.get("IMG_PREDICTION_REPO"),  os.environ.get("ML_MODEL_WEIGHTS_DIR"), os.environ.get("ML_MODEL_RESULTS_DIR"))
     inference.start()

if __name__ == '__main__':
    try:
       startInferenceController()
    except KeyboardInterrupt:
        pass