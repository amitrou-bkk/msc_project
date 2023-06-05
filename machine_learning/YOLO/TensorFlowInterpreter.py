import tensorflow as tf
import cv2
import numpy as np
import random
import yolov5
#References to the following
# https://github.com/neso613/yolo-v5-tflite-model
class TensorFlowInterpreter:
    def __init__(self, tfliteModel):
        self.__interpreter = tf.lite.Interpreter(model_path=tfliteModel)
    def test() :
        x = yolov5.YOLOv5()
        x.predict()
    def Predict(self, data, original_image, dataFn = None):
        #Allocate tensors.
        self.__interpreter.allocate_tensors()
        # Get input and output tensors.
        input_details = self.__interpreter.get_input_details()
        output_details = self.__interpreter.get_output_details()

        print(input_details)
        print(output_details)

        print(data.shape)

        # Test the model on random input data.
        input_shape = input_details[0]['shape']
        input_index = input_details[0]['index']
        self.__interpreter.set_tensor(input_index, data)
        self.__interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
    
        pred = self.__interpreter.get_tensor(output_details[0]['index'])

        names = ["mask", "no mask"]
        colors = {
            name: [random.randint(0, 255) for _ in range(3)] for i, name in enumerate(names)
        }
        ori_images = [original_image.copy()]
        image, ratio, dwdh = TensorFlowInterpreter.letterbox(original_image.copy(), auto=False)
        for i, (batch_id, x0, y0, x1, y1, cls_id, score) in enumerate(pred):
            image = ori_images[int(batch_id)]
            box = np.array([x0, y0, x1, y1])
            box -= np.array(dwdh * 2)
            box /= ratio
            box = box.round().astype(np.int32).tolist()
            cls_id = int(cls_id)
            score = round(float(score), 3)
            name = names[cls_id]
            color = colors[name]
            name += " " + str(score)
            cv2.rectangle(image, box[:2], box[2:], color, 2)
            cv2.putText(
                image,
                name,
                (box[0], box[1] + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                [225, 255, 255],
                thickness=2)
        cv2.imshow("test", ori_images[0])
        cv2.waitKey(0)
        
        
        print(pred.shape)
        # pred[..., 0] *= 416  # x
        # pred[..., 1] *= 416  # y
        # pred[..., 2] *= 416  # w
        # pred[..., 3] *= 416 # h
        results = np.squeeze(pred)
        detections = tf.image.combined_non_max_suppression(
            boxes=tf.expand_dims(pred[..., :4], axis=2),
            scores=pred[..., 4:5],
            max_output_size_per_class=100,
            max_total_size=100,
            iou_threshold=0.45,
            score_threshold=0.25
        )

       

        boxes = detections.nmsed_boxes[detections.nmsed_scores[:, 0] > 0.25]
        g = boxes.numpy()
        scores = detections.nmsed_scores[:, 0][detections.nmsed_scores[:, 0] > 0.25]
        classes = detections.nmsed_classes[detections.nmsed_scores[:, 0] > 0.25]
        boxes[0]
        print(boxes)
        print(scores)
        print(classes)

        xyxy, classes, scores = TensorFlowInterpreter.YOLOdetect(pred)
        for i in range(len(scores)):
            if ((scores[i] >= 0.9) and (scores[i] <= 1.0)):
                H = 416
                W = 416
                xmin = int(max(1,(xyxy[0][i] * W)))
                ymin = int(max(1,(xyxy[1][i] * H)))
                xmax = int(min(H,(xyxy[2][i] * W)))
                ymax = int(min(W,(xyxy[3][i] * H)))
                print((xmin, ymin, xmax, ymax))
                print(classes[i])
                mage = cv2.rectangle(original_image, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
                cv2.imshow("window_name", mage) 
        cv2.waitKey(0)
        # detection_scores = self.__interpreter.get_tensor(output_details[2]['index'])
        # num_detections : self.__interpreter.get_tensor(output_details[3]['index'])
        # print(pred)
        
        # for label, idx in train_data_gen.class_indices.items():  
        #     if top_k[idx]==1:
        #         print("Prediction: " label)
    def classFilter(classdata):
        classes = []  # create a list
        for i in range(classdata.shape[0]):         # loop through all predictions
            classes.append(classdata[i].argmax())   # get the best classification location
        return classes  # return classes (int)
    def YOLOdetect(output_data):  # input = interpreter, output is boxes(xyxy), classes, scores
        output_data = output_data[0]                # x(1, 25200, 7) to x(25200, 7)
        boxes = np.squeeze(output_data[..., :4])    # boxes  [25200, 4]
        scores = np.squeeze( output_data[..., 4:5]) # confidences  [25200, 1]
        classes = TensorFlowInterpreter.classFilter(output_data[..., 5:]) # get classes
    #    Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
        x, y, w, h = boxes[..., 0], boxes[..., 1], boxes[..., 2], boxes[..., 3] #xywh
        xyxy = [x - w / 2, y - h / 2, x + w / 2, y + h / 2]  # xywh to xyxy   [4, 25200]

        return xyxy, classes, scores  # output is boxes(x,y,x,y), classes(int), scores(float) [predictions length]
    def letterbox(im, new_shape=(416, 416), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
        # Resize and pad image while meeting stride-multiple constraints
        shape = im.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better val mAP)
            r = min(r, 1.0)

        # Compute padding
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(
            im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color
        )  # add border
        return im, r, (dw, dh)
    def filter_boxes(self, box_xywh, scores, score_threshold=0.4, input_shape = tf.constant([416,416])):
            scores_max = tf.math.reduce_max(scores, axis=-1)

            mask = scores_max >= score_threshold
            class_boxes = tf.boolean_mask(box_xywh, mask)
            pred_conf = tf.boolean_mask(scores, mask)
            class_boxes = tf.reshape(class_boxes, [tf.shape(scores)[0], -1, tf.shape(class_boxes)[-1]])
            pred_conf = tf.reshape(pred_conf, [tf.shape(scores)[0], -1, tf.shape(pred_conf)[-1]])

            box_xy, box_wh = tf.split(class_boxes, (2, 2), axis=-1)

            input_shape = tf.cast(input_shape, dtype=tf.float32)

            box_yx = box_xy[..., ::-1]
            box_hw = box_wh[..., ::-1]

            box_mins = (box_yx - (box_hw / 2.)) / input_shape
            box_maxes = (box_yx + (box_hw / 2.)) / input_shape
            boxes = tf.concat([
                box_mins[..., 0:1],  # y_min
                box_mins[..., 1:2],  # x_min
                box_maxes[..., 0:1],  # y_max
                box_maxes[..., 1:2]  # x_max
            ], axis=-1)
            # return tf.concat([boxes, pred_conf], axis=-1)
            return (boxes, pred_conf)

def preprocessImage(img):
    img = cv2.resize(img, (416, 416), interpolation = cv2.INTER_AREA)
    ##img = img[:, :, ::-1].astype('float32')  # BGR to RGB, to 3x416x416
    img= np.expand_dims(img, axis=0)
    #img = np.ascontiguousarray(img)
    #img /= 255
    #img = img.astype('float32') / 255
    return img.astype('float32')
#     img = cv2.imread(image_path)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     image = img.copy()
#     image = image.transpose((2, 0, 1))
#     image = np.expand_dims(image, 0)
#     image = np.ascontiguousarray(image)

#     im = image.astype(np.float32)
#     im /= 255
#     return im



print(tf.__version__)
customInterpreter = TensorFlowInterpreter(tfliteModel="/home/amitrou/msc_project/src/machine_learning/YOLO/20230423172055-best-fp16.tflite")
original_img = cv2.imread("/home/amitrou/msc_project/src/machine_learning/YOLO/20230423172922-maksssksksss692.png") 
proc_img=preprocessImage(original_img)
output=customInterpreter.Predict(proc_img, original_img)
