import tensorflow as tf
from numpy import expand_dims, squeeze
import numpy as np
import cv2
import imutils

import cv2
import numpy as np
from matplotlib import pyplot as plt

import math

def head_hand_distance_possibility(head_box, frame):

    if head_box != None:

        x, y, w, h = head_box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)

        center_x = int(x+w / 2)
        center_y = int(y+h * 2)

        cv2.circle(frame, (center_x, center_y), 1, (0, 0, 255), 1)

        #hight head to cm
        head = (y+h) / 37.79527559055
        #ratio 30 mean head / current head
        head = 30 / head

        #64 + 10 approx arm / ratio head
        arm = (64 + 10) / head
        #arm to pixel
        arm = int(arm * 37.79527559055)
        #region arm possible
        cv2.circle(frame, (center_x, center_y), arm, (0, 0, 255), 1)



def hand_possibility(hand, head, frame):

    x, y, w, h = hand

    
    center_x = int( (x+w) / 2)
    center_y = int( (y+h) / 2)
    #cv2.circle(frame, (center_x, center_y), 1, (255, 0, 0), 5)

    #head ratio
    x1, y1, w1, h1 = head
    head = (y1+h1) / 37.79527559055
    #ratio 30 mean head / current head
    head = 30 / head

    #arm distance 20 cm possibility to move
    arm = int( (20 * 37.79527559055) / head)
    cv2.circle(frame, (center_x, center_y), arm, (255, 0, 0), 5)
    

# Load a frozen infrerence graph into memory
def load_inference_graph(path_to_ckpt):
    # load frozen tensorflow model into memory
    detection_graph = tf.Graph()

    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(path_to_ckpt, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.compat.v1.Session(graph=detection_graph)
    return detection_graph, sess




def detect_objects(image_np, detection_graph, sess):


    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    image_np_expanded = expand_dims(image_np, axis=0)

    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')

    (boxes, scores) = sess.run([detection_boxes, detection_scores],
                               feed_dict={image_tensor: image_np_expanded})

    return squeeze(boxes), squeeze(scores)


def hands_detections(scores, boxes, frame):
    """We detect hands, by position we define if it are to left or to right.
    Recup it for history if we have impossible detections"""

    height, width = frame.shape[:2]
    detections = [(int(boxes[i][1] * width), int(boxes[i][0] * height),
                   int(boxes[i][3] * width), int(boxes[i][2] * height))
                   for i in range(2) if (scores[i] > 0.10)]

    return detections


def make_line(thresh, margin):
    """We make line for detect more than one area
    with border, on eyelashes is paste to the border"""



    cv2.line(thresh, (0, 0), (0, thresh.shape[0]), (255, 255, 255), margin)
    cv2.line(thresh, (0, 0), (thresh.shape[1], 0), (255, 255, 255), margin)
    cv2.line(thresh, (thresh.shape[1], 0), (thresh.shape[1], thresh.shape[0]), (255, 255, 255), margin)
    cv2.line(thresh, (0,  thresh.shape[0]), (thresh.shape[1], thresh.shape[0]), (255, 255, 255), margin)




def skin_detector(region, frame):

    nb = 35

    crop = frame[region[1] - nb:region[3] + nb, region[0] - nb:region[2] + nb]
    crop_convex = crop.copy()

    #crop = cv2.blur(crop, (5, 5))

    min_YCrCb = np.array([0,140,85],np.uint8)
    max_YCrCb = np.array([240,180,130],np.uint8)
    imageYCrCb = cv2.cvtColor(crop, cv2.COLOR_BGR2YCR_CB)
    skinRegionYCrCb = cv2.inRange(imageYCrCb,min_YCrCb,max_YCrCb)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    skinMask = cv2.dilate(skinRegionYCrCb, kernel, iterations = 2)
    skinMask = cv2.morphologyEx(skinMask, cv2.MORPH_CLOSE, kernel)

    skinYCrCb = cv2.bitwise_and(crop, crop, mask = skinMask)


    gray = cv2.cvtColor(skinYCrCb, cv2.COLOR_BGR2GRAY)
    contours = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
    contours = sorted(contours, key=cv2.contourArea)

    for nb, cnts in enumerate(contours):
        if nb < len(contours) - 1:
            hull = cv2.convexHull(cnts)
            cv2.drawContours(skinYCrCb, [hull], -1, (0, 0, 255), 1)
            cv2.fillPoly(skinYCrCb, [hull], (0, 0, 0))



    gray = cv2.cvtColor(skinYCrCb, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    make_line(thresh, 5)

    contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
    contours = sorted(contours, key=cv2.contourArea)

    for nb, cnts in enumerate(contours):
        if nb <  len(contours) - 2:
            cv2.fillPoly(thresh, [cnts], (255, 255, 255))


    cv2.imshow("thresh", thresh)

    contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
    contours = sorted(contours, key=cv2.contourArea)
    for nb, cnts in enumerate(contours):
        if nb <  len(contours) - 2:
            cv2.fillPoly(thresh, [cnts], (0, 0, 0))


    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    morph_img = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours = cv2.findContours(morph_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
    contours = sorted(contours, key=cv2.contourArea)
    for nb, cnts in enumerate(contours):
        if nb <  len(contours) - 2:
            cv2.fillPoly(morph_img, [cnts], (255, 255, 255))


    contours = cv2.findContours(morph_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
    contours = sorted(contours, key=cv2.contourArea)

    [cv2.drawContours(morph_img, [i], -1 , (255, 255, 255), 2) for i in contours]


    cv2.imshow("morph_img", morph_img)







##
##
##
##
##
##
##
##
##    kernel = np.ones((3,3),np.uint8)
##    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
##
##    make_line(opening)
##
##    contours = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
##    contours = sorted(contours, key=cv2.contourArea)
##
##    cv2.fillPoly(crop, [contours[-2]], (79, 220, 25))
##    cv2.drawContours(crop, [contours[-2]], -1 , (0, 0, 0), 1)
##
##
##
##    acc = 0.02 * cv2.arcLength(contours[-2], True)
##    approx = cv2.approxPolyDP(contours[-2], acc, True)
##
##    hull = cv2.convexHull(approx, returnPoints=False)
##    hull_draw = cv2.convexHull(approx)
##
##    cv2.drawContours(crop_convex, [hull_draw], -1 , (255, 0, 0), 1)
##    cv2.drawContours(crop_convex, [approx], -1 , (0, 0, 255), 1)
##
##
##    cv2.imshow("crop_convex", crop_convex)
##
##
##
##    M = cv2.moments(contours[-2])
##    cX = int(M["m10"] / M["m00"])
##    cY = int(M["m01"] / M["m00"])
##
##
##    cv2.circle(crop_convex, (cX, cY), 1, (0, 0, 255), 2)
##










def hand(frame, detection_graph, sess, head_box):


    #head_hand_distance_possibility(head_box, frame)

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes, scores = detect_objects(frameRGB, detection_graph, sess)

    detections = hands_detections(scores, boxes, frame)

    for nb, hand in enumerate(detections):

        skin_detector(hand, frame)

        #cv2.rectangle(frame, (hand[0], hand[1]), (hand[2], hand[3]), (79, 220, 25), 4)
        #hand_possibility(hand, head_box, frame)

        #cv2.imshow(str(nb), crop_thresh)

















































