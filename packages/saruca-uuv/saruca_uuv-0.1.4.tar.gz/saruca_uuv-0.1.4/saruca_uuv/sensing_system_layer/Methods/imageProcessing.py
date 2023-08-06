# object data
# distance data
import cv2
import numpy as np
from ..Classes.EntityLayer import EntityLayer


def circleAndRectangleDetection():
    """
        Detection
    """
    captureFrame = cv2.VideoCapture("<VIDEO PATH>")
    while True:
        ret, frame = captureFrame.read()

        # frame = cv2.flip(frame, 1)
        # frame = cv2.resize(frame, (960, 720))

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        frameBlob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), swapRB=True, crop=False)

        labels = ["rectangle", "circle"]

        colors = ["0, 0, 255", "0, 0, 255", "255, 0, 0", "255, 255, 0", "0, 255, 0"]
        colors = [np.array(color.split(",")).astype("int") for color in colors]
        colors = np.array(colors)
        colors = np.tile(colors, (18, 1))

        model = cv2.dnn.readNetFromDarknet("<CFG FILE PATH>", "<WEIGHTS FILE PATH>")

        layers = model.getLayerNames()
        outputLayer = [layers[layer[0] - 1] for layer in model.getUnconnectedOutLayers()]

        model.setInput(frameBlob)

        detectionLayers = model.forward(outputLayer)

        idsList = []
        boxesList = []
        confidencesList = []

        for detectionLayer in detectionLayers:
            for objectDetection in detectionLayer:
                scores = objectDetection[5:]
                predictedId = np.argmax(scores)
                confidence = scores[predictedId]

                if confidence > 0.7:
                    label = labels[predictedId]
                    boundingBox = objectDetection[0:4] * np.array([frameWidth, frameHeight, frameWidth, frameHeight])
                    (boxCenterX, boxCenterY, boxWidth, boxHeight) = boundingBox.astype("int")

                    startX = int(boxCenterX - (boxWidth / 2))
                    startY = int(boxCenterY - (boxHeight / 2))

                    idsList.append(predictedId)
                    confidencesList.append(float(confidence))
                    boxesList.append([startX, startY, int(boxWidth), int(boxHeight)])

        maxIds = cv2.dnn.NMSBoxes(boxesList, confidencesList, 0.5, 0.4)

        for maxId in maxIds:
            maxClassId = maxId[0]
            box = boxesList[maxClassId]

            startX = box[0]
            startY = box[1]
            boxWidth = box[2]
            boxHeight = box[3]

            predictedId = idsList[maxClassId]
            label = labels[predictedId]
            confidence = confidencesList[maxClassId]

            endX = startX + boxWidth
            endY = startY + boxHeight

            boxColor = colors[predictedId]
            boxColor = [int(each) for each in boxColor]

            label = "{}: {:.2f}%".format(label, confidence * 100)
            # print("predicted object {}".format(label))

            cv2.rectangle(frame, (startX, startY), (endX, endY), boxColor, 2)
            cv2.rectangle(frame, (startX - 1, startY), (endX + 1, startY - 30), boxColor, -1)
            cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.5, (255, 255, 255), 2)

        if cv2.waitKey(1) & ord("q") == 27:
            break
        cv2.imshow("Tespit Edilen", frame)
    captureFrame.release()
    cv2.destroyAllWindows()


# sample usage
imageObject = EntityLayer((25, 15), "rectangle", 12, "trapezium")
print(imageObject.getBoundingBoxes())
print("Goruntu isleme metodu calistirildi...")
# circleAndRectangleDetection()
