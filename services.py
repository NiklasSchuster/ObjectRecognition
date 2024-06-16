import os
import cv2
import numpy as np
import base64

cfg_path = os.path.join(".", "yolo_tiny_configs", "yolov3-tiny.cfg")
weights_path = os.path.join(".", "yolo_tiny_configs", "yolov3-tiny.weights")
names_path = os.path.join(".", "yolo_tiny_configs", "coco.names")


class ObjectDetector:
     @staticmethod
     def detect_objects(img):
        nparr = np.fromstring(base64.b64decode(img), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        with open(names_path, 'r') as file:
            class_names = [line.strip() for line in file.readlines()]

        net = cv2.dnn.readNetFromDarknet(cfg_path, weights_path)
        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), True)
        net.setInput(blob)

        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

        outs = net.forward(output_layers)
        outputs = [c for out in outs for c in out if c[4] > 0.1]
        boxes = []
        class_ids = []
        scores = []

        for detection in outputs:
            box = detection[:4]
            x,y,w,h = box
            box = [int(x * width), int(y * height), int(w * width), int(h * height)]

            class_id = np.argmax(detection[5:])
            score = np.amax(detection[5:])
            if score > 0:
                boxes.append(box)
                class_ids.append(class_id)
                scores.append(score)

        labels = []
        accuracies = []
        for i, box in enumerate(boxes):
            x,y,w,h = box
            labels.append(str(class_names[class_ids[i]]))
            accuracies.append(scores[i])

        labels = list(map(str, labels))
        accuracies = list(map(float, accuracies))

        objects = []
        for i, n in enumerate(labels):
            objects.append({"label": labels[i], "accuracy": accuracies[i]})
        return objects


