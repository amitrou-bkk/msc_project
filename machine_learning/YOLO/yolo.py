
import numpy as np
import os
import yolov5
import torch
import cv2


class YOLOEmbeddedOpenCv:
    scale = 0.00392
    default_cfg_file = os.path.join(os.path.dirname(__file__), "yolo3.cfg")
    default_classes_file = os.path.join(os.path.dirname(__file__), "classes.txt")
    default_weights_file = os.path.join(os.path.dirname(__file__), "yolov3.weights")

    def __init__(self, config = None, classes = None, weights = None) :
        self.cfgFile = YOLOEmbeddedOpenCv if config == None else config
        self.classesFile =  YOLOEmbeddedOpenCv.default_classes_file if classes == None else classes
        self.weightsFile = YOLOEmbeddedOpenCv.default_weights_file if weights == None else weights

    def createModel(self):
        with open(self.classesFile, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        # read pre-trained model and config file
        self.net = cv2.dnn.readNet(self.weightsFile, self.cfgFile)
        return self.net


    def predict(self, imageFile):
        image = cv2.imread(imageFile)

        Width = image.shape[1]
        Height = image.shape[0]
        blob = cv2.dnn.blobFromImage(image, YOLOEmbeddedOpenCv.scale, (416,416), (0,0,0), True, crop=False)

        # set input blob for the network
        self.net.setInput(blob)
        layer_names = self.net.getLayerNames()

        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        outs = self.net.forward(output_layers)

        # initialization
        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4
        results = []
        # for each detetion from each output layer
        # get the confidence, class id, bounding box params
        # and ignore weak detections (confidence < 0.5)
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            results.append((self.classes[class_ids[i]], confidences[i], box))

        return results

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