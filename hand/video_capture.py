import tensorflow as tf
from utils import load_inference_graph, detect_objects
import numpy as np
import cv2

print(tf.version.VERSION)



def hands_detections(scores, boxes, frame):
    """We detect hands, by position we define if it are to left or to right.
    Recup it for history if we have impossible detections"""

    width = 500; height = 400
    detections = [(int(boxes[i][1] * width), int(boxes[i][0] * height),
                   int(boxes[i][3] * width), int(boxes[i][2] * height))
                   for i in range(2) if (scores[i] > 0.10)]

    return detections









def video_capture(video_name, hand_model):

    detection_graph, sess = load_inference_graph(hand_model)

    video = cv2.VideoCapture(video_name)
    fgbg = cv2.createBackgroundSubtractorMOG2(history=120, varThreshold = 120, detectShadows=False)

    historic = []

    protoFile = "pose_deploy.prototxt"
    weightsFile = "pose_iter_102000.caffemodel"

    while True:

        frame = cv2.resize(video.read()[1], (500, 400))
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        boxes, scores = detect_objects(frameRGB, detection_graph, sess)
        detections = hands_detections(scores, boxes, frame)


        for hand in detections:
            if len(hand) > 0:
                #cv2.rectangle(frame, (hand[0], hand[1]), (hand[2], hand[3]), (79, 220, 25), 4)

                oh = frame[hand[1]:hand[3], hand[0]:hand[2]]

                nPoints = 22
                POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]
                net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

                frameCopy = np.copy(oh)
                frameWidth = oh.shape[1]
                frameHeight = oh.shape[0]
                aspect_ratio = frameWidth/frameHeight

                threshold = 0.1


                # input image dimensions for the network
                inHeight = 368
                inWidth = int(((aspect_ratio*inHeight)*8)//8)
                inpBlob = cv2.dnn.blobFromImage(oh, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)

                net.setInput(inpBlob)

                output = net.forward()


                # Empty list to store the detected keypoints
                points = []

                for i in range(nPoints):
                    # confidence map of corresponding body's part.
                    probMap = output[0, i, :, :]
                    probMap = cv2.resize(probMap, (frameWidth, frameHeight))

                    # Find global maxima of the probMap.
                    minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

                    if prob > threshold :
                        cv2.circle(frameCopy, (int(point[0]), int(point[1])), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                        cv2.putText(frameCopy, "{}".format(i), (int(point[0]), int(point[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)

                        # Add the point to the list if the probability is greater than the threshold
                        points.append((int(point[0]), int(point[1])))
                    else :
                        points.append(None)

                # Draw Skeleton
                for pair in POSE_PAIRS:
                    partA = pair[0]
                    partB = pair[1]

                    if points[partA] and points[partB]:
                        cv2.line(oh, points[partA], points[partB], (0, 255, 255), 2)
                        cv2.circle(oh, points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
                        cv2.circle(oh, points[partB], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)


                cv2.imshow('Output-Keypoints', frameCopy)
                cv2.imshow('Output-Skeleton', oh)
                cv2.waitKey(0)









        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        frame += 1

    video.release()
    cv2.destroyAllWindows()





















