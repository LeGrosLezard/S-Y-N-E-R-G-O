import cv2
import tensorflow as tf
import numpy as np
from time import time
import imutils
from utils import load_inference_graph, detect_objects


print(tf.version.VERSION)



def hands_detections(scores, boxes, frame):
    """We detect hands, by position we define if it are to left or to right.
    Recup it for history if we have impossible detections"""

    for i in range(2):
        if (scores[i] > 0.10):
            (left, right, top, bottom) = (boxes[i][1] * 500, boxes[i][3] * 500,
                                          boxes[i][0] * 400, boxes[i][2] * 400)
            p1 = (int(left), int(top))
            p2 = (int(right), int(bottom))
            #cv2.rectangle(frame, p1, p2, (0, 0, 0), 4)

    detected_points = [(int(boxes[i][1] * 500), int(boxes[i][3] * 500),
                        int(boxes[i][0] * 400), int(boxes[i][2] * 400)) for i in range(2) if scores[i] > 0.10]

    right_left_points = [  [(pt[0], pt[2], pt[1], pt[3]) for pt in detected_points if pt[0] < 250],
                           [(pt[0], pt[2], pt[1], pt[3]) for pt in detected_points if pt[0] > 250]   ]
    print(right_left_points)
    return right_left_points


def skin_color(hand):

    min_YCrCb = np.array([0,140,85],np.uint8)
    max_YCrCb = np.array([240,180,130],np.uint8)

    imageYCrCb = cv2.cvtColor(hand,cv2.COLOR_BGR2YCR_CB)
    skinRegionYCrCb = cv2.inRange(imageYCrCb,min_YCrCb,max_YCrCb)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    skinMask = cv2.dilate(skinRegionYCrCb, kernel, iterations = 2)

    skinYCrCb = cv2.bitwise_and(hand, hand, mask = skinMask)

    return skinYCrCb



def video_capture(video_name, hand_model):

    ok = False
    detection_graph, sess = load_inference_graph(hand_model)
    video = cv2.VideoCapture(video_name)
    fgbg = cv2.createBackgroundSubtractorMOG2(history=80, varThreshold = 20, detectShadows=False)


    while True:

        frame = cv2.resize(video.read()[1], (500, 400))
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        br = fgbg.apply(frame)

        back = cv2.bitwise_and(frame, frame, mask = br)


        cv2.imshow("back", back)


        boxes, scores = detect_objects(frameRGB, detection_graph, sess)
        a = hands_detections(scores, boxes, frame)

        c = 0
        for i in a:
            if len(i) > 0:
                nb = 15



                roi = frame[ i[0][1]-nb : i[0][3]+nb, i[0][0]-nb : i[0][2]+nb ]
                
##                roiback = back[ i[0][1]-nb : i[0][3]+nb, i[0][0]-nb : i[0][2]+nb ]
##                cv2.imshow("roiback", roiback)


                try:
                    min_YCrCb = np.array([0,140,85],np.uint8)
                    max_YCrCb = np.array([240,180,130],np.uint8)

                    imageYCrCb = cv2.cvtColor(roi,cv2.COLOR_BGR2YCR_CB)
                    skinRegionYCrCb = cv2.inRange(imageYCrCb,min_YCrCb,max_YCrCb)

                    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
                    skinMask = cv2.dilate(skinRegionYCrCb, kernel, iterations = 2)

                    skinYCrCb = cv2.bitwise_and(roi, roi, mask = skinMask)

                    cv2.imshow("skinYCrCb", skinYCrCb)


                except:
                    pass




##                imgray = cv2.cvtColor(skinYCrCb, cv2.COLOR_BGR2GRAY)
##                for thresh in range(5, 150, 5):
##
##
##                    print(thresh)
##                    ret, thresh = cv2.threshold(imgray, thresh, 255, 0)
##                                    
##                    cv2.imshow("roi", frame)
##                    cv2.waitKey(0)

                imgray = cv2.cvtColor(skinYCrCb, cv2.COLOR_BGR2GRAY)
                ret, thresh = cv2.threshold(imgray, 100, 255, 0)
                cv2.imshow("thresh", thresh)

                contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

                for i in contours:
                    print(cv2.contourArea(i))
                    cv2.drawContours(roi, [i], -1, (0,255,0), 3)
                
##                    cv2.imshow("roi", frame)
##                    cv2.waitKey(0)







        cv2.imshow("mask", frame)
        if cv2.waitKey(0) & 0xFF == ord("q"):
            break



    video.release()
    cv2.destroyAllWindows()





















