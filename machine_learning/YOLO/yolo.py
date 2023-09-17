
import numpy as np
import os
import torch
import cv2

class LocalYoloModel:
    def __init__(self, yolo_model_path, custom_weights_path, classes):

        if not os.path.exists(custom_weights_path):
            raise Exception("Weights for model where not found")

        if not os.path.exists(yolo_model_path):
            raise Exception("Model was not found")
        
        self.model = torch.hub.load(yolo_model_path, 'custom', path=custom_weights_path, source='local') 
        self.classes = classes

    def predict(self, imagePath, showPrediction = False, confidence_base = 0):
        result = []
        model_results = self.model(imagePath)
        inference_results = model_results.pandas().xyxy[0].values
        cvImage = cv2.imread(imagePath) 
        
        for i in range(len(inference_results)):
            xMin = inference_results[i][0]
            yMin = inference_results[i][1]
            xMax = inference_results[i][2]
            yMax = inference_results[i][3]
            confidence = inference_results[i][4]
            classIndex = inference_results[i][5]
            upperLeftPoint = int(xMin), int(yMin)
            lowerRightPoint = int(xMax), int(yMax)
            class_name = self.classes[classIndex]

            if confidence >= confidence_base:
                result.append((upperLeftPoint, lowerRightPoint, confidence, class_name))

            if showPrediction:
                cvImage = cv2.rectangle(cvImage, upperLeftPoint, lowerRightPoint, (255, 0, 0), 2)
                positionText = int(xMin), int(yMin) + 20
                cv2.putText(cvImage, str(confidence), positionText, cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255, 0, 0), 1, cv2.LINE_AA)
                
        if (showPrediction):
            print(result)
            cv2.imshow("test", cvImage)
            cv2.waitKey(0)
        else:
            return result
    
# if __name__ == "__main__":
#     print("Running example inference")
#     model = LocalYoloModel("/home/amitrou/msc_project/src/machine_learning/YOLO/custom_weights/20230521110311-best.pt", ['mask', 'no mask'])
#     model.predict( os.path.join(os.path.dirname(__file__), "image_510.jpg"), True)