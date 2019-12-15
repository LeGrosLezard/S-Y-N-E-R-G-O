from cv2 import VideoCapture, resize, cvtColor, COLOR_BGR2RGB, imshow, waitKey, destroyAllWindows, rectangle
from hand_detection.utils import load_inference_graph, detect_objects
from hand_detection.hand_detection import hands_detections
#from hand_signification.skelettor import make_skelettor

import cv2
import numpy as np

def skin_detector(crop):
    min_YCrCb = np.array([0,140,85],np.uint8)
    max_YCrCb = np.array([240,180,130],np.uint8)
    imageYCrCb = cv2.cvtColor(crop, cv2.COLOR_BGR2YCR_CB)
    skinRegionYCrCb = cv2.inRange(imageYCrCb,min_YCrCb,max_YCrCb)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    skinMask = cv2.dilate(skinRegionYCrCb, kernel, iterations = 2)

    skinYCrCb = cv2.bitwise_and(crop, crop, mask = skinMask)

    return skinYCrCb


def video_capture(video_name, hand_model, hand_skelettor_PROTXT, hand_skelettor_CAFFE):

    detection_graph, sess = load_inference_graph(hand_model)
    video = VideoCapture(video_name)

    blank_image = np.zeros((400,500,3), np.uint8)
    blank_image[0:, 0:] = 0, 0, 0

    counter = 0

    while True:

        if counter == 10:
            blank_image[0:, 0:] = 0, 0, 0
            counter = 0

        frame = resize(video.read()[1], (500, 400))
        copy = frame.copy()

        frameRGB = cvtColor(frame, COLOR_BGR2RGB)

        boxes, scores = detect_objects(frameRGB, detection_graph, sess)
        detections = hands_detections(scores, boxes, frame)

        nb = 0
        for hand in detections:
            if len(hand) > 0:
                rectangle(copy, (hand[0] - nb, hand[1] - nb), (hand[2] + nb, hand[3] + nb), (79, 220, 25), 4)
                rectangle(blank_image, (hand[0] - nb, hand[1] - nb), (hand[2] + nb, hand[3] + nb), (79, 220, 25), 4)

                #crop = frame[hand[1] - nb : hand[3] + nb, hand[0] - nb: hand[2] + nb]






        imshow("frame", copy)
        imshow("dzada", blank_image)
        if waitKey(0) & 0xFF == ord("q"):
            break

        counter += 1
    video.release()
    cv2.destroyAllWindows()





















