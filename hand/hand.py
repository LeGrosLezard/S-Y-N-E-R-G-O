import tensorflow as tf
from numpy import expand_dims, squeeze
import numpy as np
import cv2
import imutils

import cv2
import numpy as np
from matplotlib import pyplot as plt

import math
import time



from sys import exit
from scipy import ndimage as ndi
from skimage.morphology import watershed, disk
from skimage import data
from skimage.io import imread
from skimage.filters import rank
from skimage.color import rgb2gray
from skimage.util import img_as_ubyte


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


def make_bitwise(contours, crop):

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    mask = np.zeros_like(gray)
    cv2.fillPoly(mask, [contours[-2]], 255)
    crop = cv2.bitwise_and(crop, crop, mask=mask)

    x, y, w, h = cv2.boundingRect(contours[-2])

    return crop


def hand_skelettor(crop, protoFile, weightsFile):

    t = time.time()

    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

    threshold = 0.1
    POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],
                   [11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]

    crop_copy = crop.copy()
    

    frameHeight, frameWidth = crop.shape[:2]
    aspect_ratio = frameWidth/frameHeight

    inHeight = 250
    inWidth = int(((aspect_ratio*inHeight)*8)//8)

    inpBlob = cv2.dnn.blobFromImage(crop, 1.0/500, (inWidth, inHeight),
                                    (0, 0, 0), swapRB=False, crop=False)

    net.setInput(inpBlob)
    output = net.forward()

    points = []      
    for i in range(22):
        # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]
        probMap = cv2.resize(probMap, (frameWidth, frameHeight))

        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        if prob > threshold :
            points.append((int(point[0]), int(point[1])))
        else :
            points.append(None)


    skeletton = [(nb) for nb, pair in enumerate(POSE_PAIRS) if points[pair[0]] and points[pair[1]]]


    # Draw Skeleton
    skeletton = []
    for nb, pair in enumerate(POSE_PAIRS):
        partA = pair[0]
        partB = pair[1]

        if points[partA] and points[partB]:
            cv2.line(crop, points[partA], points[partB], (0, 255, 255), 2)
            cv2.circle(crop, points[partA], 4, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.circle(crop, points[partB], 4, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

            skeletton.append(nb)

    cv2.imshow("skel", crop)


    print("time taken by network : {:.3f}".format(time.time() - t))

    return skeletton


def treat_skeletton_points(skeletton):
    pass


def hand(frame, detection_graph, sess, head_box):

    frame_copy = frame.copy()

    #head_hand_distance_possibility(head_box, frame)

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes, scores = detect_objects(frameRGB, detection_graph, sess)

    detections = hands_detections(scores, boxes, frame)

    for nb, hand in enumerate(detections):

        skinYCrCb, crop, copy = skin_detector(hand, frame, frame_copy)
        copy = crop.copy()

        contours = hand_treatment(skinYCrCb, crop)
        copy = make_bitwise(contours, copy)


        protoFile = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handa\models\pose_deploy.prototxt"
        weightsFile = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handa\models\pose_iter_102000.caffemodel"

        points = hand_skelettor(copy, protoFile, weightsFile)
        treat_skeletton_points(points)

        
        cv2.imshow("crop", crop)
        cv2.waitKey(0)






    #cv2.imshow("crop_convex", frame_copy)













































