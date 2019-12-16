from cv2 import VideoCapture, resize, cvtColor, COLOR_BGR2RGB, imshow, waitKey, destroyAllWindows, rectangle
from hand_detection.utils import load_inference_graph, detect_objects
from hand_detection.hand_detection import hands_detections
#from hand_signification.skelettor import make_skelettor

import cv2
import numpy as np


def recup_YCrCb(frame):
    pass




def skin_detector(crop):
    min_YCrCb = np.array([0,140,85],np.uint8)
    max_YCrCb = np.array([240,180,130],np.uint8)
    imageYCrCb = cv2.cvtColor(crop, cv2.COLOR_BGR2YCR_CB)
    skinRegionYCrCb = cv2.inRange(imageYCrCb,min_YCrCb,max_YCrCb)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    skinMask = cv2.dilate(skinRegionYCrCb, kernel, iterations = 2)

    skinYCrCb = cv2.bitwise_and(crop, crop, mask = skinMask)

    return skinYCrCb


def adjust_gamma(image, gamma):
    """We add light to the video, we play with gamma"""

    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")

    return cv2.LUT(image, table)


def recup_YCrCb(img):

    b = 0; g = 0; r = 0; counter = 0
    for i in range(img.shape[0]):
         for j in range(img.shape[1]):

             b += img[i ,j][0]
             g += img[i ,j][1]
             r += img[i ,j][2]
             counter += 1

    b = b / counter
    g = g / counter
    r = r / counter

    y = 0.299 * r
    cb = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    cr = 0.5 * r - 0.4187 * g - 0.0813 * b + 128

    print(y, cb, cr)



def area_frame(frame):
    pass


def video_capture(video_name, hand_model, hand_skelettor_PROTXT, hand_skelettor_CAFFE):

    detection_graph, sess = load_inference_graph(hand_model)
    video = VideoCapture(0)

    #subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=True)


    blank_image = np.zeros((400,500,3), np.uint8)
    blank_image[0:, 0:] = 0, 0, 0

    counter = 0
    a = 0

    while True:

        if counter == 10:
            blank_image[0:, 0:] = 0, 0, 0
            counter = 0

        frame = resize(video.read()[1], (500, 400))
        #recup_YCrCb(img) video sombre
        #frame = adjust_gamma(frame, 1.6)
        #recup_YCrCb(img)


        #video tres allumé
        #frame = adjust_gamma(frame, 0.3)


        frameRGB = cvtColor(frame, COLOR_BGR2RGB)
        aaaaaa = skin_detector(frame)

        boxes, scores = detect_objects(frameRGB, detection_graph, sess)
        detections = hands_detections(scores, boxes, frame)

        nb = 0
        for hand in detections:
            if len(hand) > 0:

                #rectangle(frame, (hand[0] - nb, hand[1] - nb), (hand[2] + nb, hand[3] + nb), (79, 220, 25), 4)
                #rectangle(blank_image, (hand[0] - nb, hand[1] - nb), (hand[2] + nb, hand[3] + nb), (79, 220, 25), 4)
                crop = frame[hand[1] - nb : hand[3] + nb, hand[0] - nb: hand[2] + nb]

                aaa = skin_detector(crop)
                imshow("aaa", aaa)






        imshow("aaaaaa", aaaaaa)


        imshow("frame", frame)
        #imshow("dzada", blank_image)

##        if waitKey(0) & 0xFF == ord("a"):
##            cv2.imwrite("a" + str(a) + ".jpg", frame)


        if waitKey(1) & 0xFF == ord("q"):
            break

        counter += 1
        a += 1
    video.release()
    cv2.destroyAllWindows()





















