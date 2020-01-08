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


def skin_detector(region, frame, frame_copy):

    size_crop = 35

    crop = frame[region[1] - size_crop:region[3] + size_crop, region[0] - size_crop:region[2] + size_crop]
    copy = frame_copy[region[1] - size_crop:region[3] + size_crop, region[0] - size_crop:region[2] + size_crop]

    #crop = cv2.blur(crop, (5, 5))

    min_YCrCb = np.array([0,140,85],np.uint8)
    max_YCrCb = np.array([240,180,130],np.uint8)
    imageYCrCb = cv2.cvtColor(crop, cv2.COLOR_BGR2YCR_CB)
    skinRegionYCrCb = cv2.inRange(imageYCrCb,min_YCrCb,max_YCrCb)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    skinMask = cv2.dilate(skinRegionYCrCb, kernel, iterations = 2)
    skinMask = cv2.morphologyEx(skinMask, cv2.MORPH_CLOSE, kernel)

    skinYCrCb = cv2.bitwise_and(crop, crop, mask = skinMask)

    return skinYCrCb, crop, copy


def make_contours(gray):

    return [sorted(cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0],
                       key=cv2.contourArea)][0]

def del_fill_contours(last_contour, contours, gray, color):

    [cv2.fillPoly(gray, [cv2.convexHull(cnts)], color) for nb, cnts in enumerate(contours)
     if nb < len(contours) - last_contour]



def hand_treatment(skinYCrCb, crop):

    copy = crop.copy()


    gray = cv2.cvtColor(skinYCrCb, cv2.COLOR_BGR2GRAY)

    #delete noise around hand
    contours = make_contours(gray)
    del_fill_contours(1, contours, skinYCrCb, (0, 0, 0) )


    #Make otsu threshold
    gray = cv2.cvtColor(skinYCrCb, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    make_line(thresh, 5)

    #Delete noise around hand on threshold
    contours = make_contours(thresh)
    del_fill_contours(2, contours, thresh, (255, 255, 255) )


    #Filled hole on hand
    contours = make_contours(thresh)
    del_fill_contours(2, contours, thresh, (0, 0, 0) )
    #contours = make_contours(thresh)


    #Close the hand
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    morph_img = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    #delete final little noise cut
    contours = make_contours(morph_img)
    del_fill_contours(2, contours, morph_img, (255, 255, 255) )

    #refinement hand contours
    contours = make_contours(morph_img)
    [cv2.drawContours(morph_img, [i], 0 , (255, 255, 255), 2) for i in contours]

    #cv2.imshow("morph_img", morph_img)


    cv2.fillPoly(crop, [contours[-2]], (79, 220, 25))
    cv2.drawContours(crop, [contours[-2]], -1 , (0, 0, 0), 2)

    contours = make_contours(morph_img)
    
    return contours



def hull(contours, crop):

##  
##    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
##
##    mask = np.zeros_like(gray)
##
##    cv2.fillPoly(mask, [contours[-2]], 255)
##    crop = cv2.bitwise_and(crop, crop, mask=mask)



    M = cv2.moments(contours[-2])
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
 
    cv2.circle(crop , (cX, cY), 2, (0, 0, 255), 2)
    cv2.imshow("crop", crop)



##    (x,y), radius = cv2.minEnclosingCircle(contours[-2])
##    center = (int(x),int(y))
##    cv2.circle(crop , center, int(radius), (255, 255, 255), 1)
##
##    cv2.imshow("crop", crop)



    acc = 0.02 * cv2.arcLength(contours[-2], True)
    approx = cv2.approxPolyDP(contours[-2], acc, True)

    hull = cv2.convexHull(approx, returnPoints=False)
    hull_draw = cv2.convexHull(approx)

    cv2.drawContours(crop, [hull_draw], -1 , (255, 0, 0), 2)
    cv2.drawContours(crop, [approx], -1 , (0, 0, 255), 2)

    


    liste_pts = []

##    copy = crop.copy()
##
    res = approx
    defects=cv2.convexityDefects(res, hull)

    cnt = 0
    for i in range(defects.shape[0]):  
        s, e, f, d = defects[i][0]
        start = tuple(res[s][0])
        end = tuple(res[e][0])
        far = tuple(res[f][0])

        cv2.circle(crop, start, 5, [0, 0, 255], -1)
        liste_pts.append(res[s][0])


    neg_top = 0
    pos_top = 0

    neg_x = 0
    pos_x = 0

    neg_ext_x = 0
    pos_ext_x = 0
    pts = 0
    for i in liste_pts:
        print(i, cX, cY)

        if i[1] - cY < 0:
            neg_top += 1
        else:
            pos_top += 1

        if i[0] - cX < 0:
            neg_x += 1
        else:
            pos_x += 1

##        if i[0] < cX - 30:
##            neg_ext_x += 1
##
##        elif i[0] > cX + 30:
##            pos_ext_x += 1
##
##        pts += 1


    out = ""
    if neg_top > pos_top: out += "haut "
    else: out += "bas "

##    if neg_ext_x > pts - 2: out += "gauche "
##    elif pos_ext_x > pts - 2: out += "droite "

    if pos_ext_x > pos_x: out += "droite"
    else: out += "gauche"

    print(out)




    
    cv2.imshow("crop", crop)
    cv2.waitKey(0)














        #cv2.circle(crop, far, 5, [211, 84, 0], -1)
        #cv2.circle(crop, end, 5, [0, 255, 0], -1)
##
##
##        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
##        b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
##        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
##        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  
##        if angle <= math.pi / 2:  
##            cnt += 1
##            cv2.circle(crop, start, 5, [0, 0, 0], -1)
##            cv2.line(crop, center, start, (255, 255, 255), 2)
##
##        if angle > math.pi / 2:  
##            cnt += 1
##            cv2.circle(crop, start, 5, [255, 255, 255], -1)
##            cv2.line(crop, center, start, (50, 240, 100), 2)
##
##


















##    cv2.imshow("copy", copy)

##    cv2.imshow("crop_pts", copy)






        

    

















def hand(frame, detection_graph, sess, head_box):

    frame_copy = frame.copy()

    #head_hand_distance_possibility(head_box, frame)

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes, scores = detect_objects(frameRGB, detection_graph, sess)

    detections = hands_detections(scores, boxes, frame)

    for nb, hand in enumerate(detections):

        skinYCrCb, crop, copy = skin_detector(hand, frame, frame_copy)
        contours = hand_treatment(skinYCrCb, crop)

        #contour from morph_img
        hull(contours, copy)

    


        #cv2.rectangle(frame, (hand[0], hand[1]), (hand[2], hand[3]), (79, 220, 25), 4)
        #hand_possibility(hand, head_box, frame)

        #cv2.imshow(str(nb), crop_thresh)



    #cv2.imshow("crop_convex", frame_copy)













































