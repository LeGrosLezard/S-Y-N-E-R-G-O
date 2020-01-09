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


from scipy.spatial import distance as dist

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
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)

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
##    del_fill_contours(2, contours, thresh, (0, 0, 0) )
##    #contours = make_contours(thresh)
##
##
##    #Close the hand
##    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
##    morph_img = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
##
##    #delete final little noise cut
##    contours = make_contours(morph_img)
##    del_fill_contours(2, contours, morph_img, (255, 255, 255) )
##
##    #refinement hand contours
##    contours = make_contours(morph_img)
##    [ for i in contours]
##
##    #cv2.imshow("morph_img", morph_img)
##
##
##    cv2.fillPoly(crop, [contours[-2]], (79, 220, 25))
##    cv2.drawContours(crop, [contours[-2]], -1 , (0, 0, 0), 2)
##
##    contours = make_contours(morph_img)
    
    return contours


def make_bitwise(contours, crop):

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    mask = np.zeros_like(gray)
    cv2.fillPoly(mask, [contours[-2]], 255)
    crop = cv2.bitwise_and(crop, crop, mask=mask)

    x, y, w, h = cv2.boundingRect(contours[-2])

    #cv2.rectangle(crop, (x, y), (x+w, y+h), (255, 0, 0), 2)

    rectangle = (x, y, w, h)

    return crop, rectangle


def hand_skelettor(crop, protoFile, weightsFile):

    t = time.time()

    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

    threshold = 0.1
    POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],
                   [11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]

    crop_copy = crop.copy()


    frameHeight, frameWidth = crop.shape[:2]
    aspect_ratio = frameWidth/frameHeight

    inHeight = 368
    inWidth = int(((aspect_ratio*inHeight)*8)//8)

    inpBlob = cv2.dnn.blobFromImage(crop, 1.0/255, (inWidth, inHeight),
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



    # Draw Skeleton
    skeletton = []
    finger = []
    position = []

    for nb, pair in enumerate(POSE_PAIRS):
        partA = pair[0]
        partB = pair[1]

        if points[partA] and points[partB]:
            cv2.line(crop_copy, points[partA], points[partB], (0, 255, 255), 2)
            cv2.circle(crop_copy, points[partA], 4, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.circle(crop_copy, points[partB], 4, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
            skeletton.append(pair)
            finger.append(nb)
            position.append((points[partA], points[partB]))
        else:
            position.append(((0, 0), (0, 0)))

    print("time taken by network : {:.3f}".format(time.time() - t))
    cv2.imshow("complete", crop_copy)
    cv2.waitKey(0)
    return skeletton, position, finger



def draw(finger, position, crop, color):
    finger = [j for i in position for j in i]
    [cv2.circle(crop, pts, 2, color, -1) for pts in finger]



def paume(pos, mid, finger):
    if len(finger) > 0 and finger[0] == 0:
        position_hand = ""
        if pos[1] > mid[0]: position_hand = "main vers haut"
        if pos[1] < mid[1]: position_hand = "main vers bas"
        print(position_hand)
        return position_hand


def hand_location(pos, finger, mid):

    hand = ""
    if len(finger) > 3 and finger[3] == 3:
        #recup hand location
        if pos[1][0] > mid[0]: hand = "main droite"
        if pos[1][0] < mid[1]: hand = "main gauche"
        print(hand)
        return hand



def palm_analyse(hand_loc, palm_center, palm, rectangle, crop, no_fng_fnd):
    """ICI main deplier ou pas"""
    copy = crop.copy()

    if no_fng_fnd is False:
        print("paume de la main")
        x, y, w, h = rectangle

        if hand_loc == "main droite": area = palm[0]
        else:area = palm[1]

        palm_area = np.array([(pts[0], pts[1]) for pts in area])
        cv2.drawContours(copy, [palm_area], 0, (0, 255, 0), 1)

        cv2.circle(copy, palm_center, 2, (255, 255, 255), 1)
        [cv2.circle(copy, pts, 2, (0, 0, 0), 1) for pts in area]

        for pts in area:
            distance = dist.euclidean(palm_center, pts)
            #print(distance)

        area = cv2.contourArea(palm_area)
        print(area)
        print(w*h)
        print("")

        cv2.imshow("palm1", copy)
        cv2.waitKey(0)


def doigt_plié(pha, phax):
    print(phax)
    if phax < 10:
        print(pha + " pliée")

    print("")







def thumb_analyse(thumb, palm, index, rectangle, crop):

    copy = crop.copy()
    cv2.circle(copy, palm, 2, (255, 255, 255), 2)
    print("pouce")
    print("")
    thumb = [j for i in thumb for j in i]
    [cv2.circle(copy, pts, 2, (0, 0, 255), 2) for pts in thumb]


    cv2.imshow("thumb", copy)
    cv2.waitKey(0)



def index_analyse(index, palm, rectangle, crop):

    print("")
    print("index")
    

    print(rectangle)
    x, y, w, h = rectangle

    copy = crop.copy()

    cv2.rectangle(copy, (x, y), (x+w, y+h), (0, 0, 255), 1)

    length = 0
    try:
        cv2.circle(copy, palm, 2, (255, 255, 255), 2)

        
        cv2.circle(copy, index[0][0], 2, (255, 0, 0), 2)
        cv2.circle(copy, index[1][0], 2, (0, 255, 0), 2)
        cv2.circle(copy, index[2][0], 2, (0, 0, 0), 2)
        cv2.circle(copy, index[2][1], 2, (0, 0, 255), 2)



        phax1 = dist.euclidean(index[0][0], index[0][1])
        cv2.line(copy, index[0][0], index[0][1], (0,0,0), 1)
        length += phax1
        doigt_plié("phalange 1", phax1)


        phax2 = dist.euclidean(index[1][0], index[1][1])
        cv2.line(copy, index[1][0], index[1][1], (0,0,0), 1)
        length += phax2
        doigt_plié("phalange 2", phax2)

        phax3 = dist.euclidean(index[2][0], index[2][1])
        cv2.line(copy, index[2][0], index[2][1], (0,0,0), 1)
        length += phax3
        doigt_plié("phalange 3", phax3)



##        (, , 137, 112)
##        26.076809620810597
##        14.866068747318506
##        14.317821063276353
##        55.260699431405456
##
##
##
##        (, , 97, 113)
##        24.20743687382041
##        17.69180601295413
##        13.45362404707371
##        55.352866933848254





#TODO
    #detecter pouce et annulaire
    #si pouce auriculaire .. index => auri -> index - > pliéq
    #changement de perspective doigt plus long -> penché vers torse et versa #531








    except:pass

    print(length)
    cv2.imshow("index", copy)
    cv2.waitKey(0)


    




def major_analyse(major, palm, rectangle, crop):

    copy = crop.copy()
    cv2.circle(copy, palm, 2, (255, 255, 255), 2)


    cv2.circle(copy, major[0][0], 2, (255, 0, 0), 2)
    cv2.circle(copy, major[1][0], 2, (0, 255, 0), 2)
    cv2.circle(copy, major[2][0], 2, (0, 0, 0), 2)
    cv2.circle(copy, major[2][1], 2, (0, 0, 255), 2)

    print("")
    print("major")

    length = 0

    phax1 = dist.euclidean(major[0][0], major[0][1])
    cv2.line(copy, major[0][0], major[0][1], (0,0,0), 1)
    length += phax1
    doigt_plié("phalange 1", phax1)

    phax2 = dist.euclidean(major[1][0], major[1][1])
    cv2.line(copy, major[1][0], major[1][1], (0,0,0), 1)
    length += phax2
    doigt_plié("phalange 2",phax2)

    phax3 = dist.euclidean(major[2][0], major[2][1])
    cv2.line(copy, major[2][0], major[2][1], (0,0,0), 1)
    length += phax3

    doigt_plié("phalange 3", phax3)



    cv2.imshow("major", copy)
    cv2.waitKey(0)





def annular_analyse(annular, palm, rectangle, crop):
    copy = crop.copy()
    cv2.circle(copy, palm, 2, (255, 255, 255), 2)

    annular = [j for i in annular for j in i]
    [cv2.circle(copy, pts, 2, (0, 0, 255), 2) for pts in annular]

    cv2.imshow("annular", copy)
    cv2.waitKey(0)
    



def auricular_analyse(auricular, palm, rectangle, crop):
    copy = crop.copy()
    cv2.circle(copy, palm, 2, (255, 255, 255), 2)

    auricular = [j for i in auricular for j in i]
    [cv2.circle(copy, pts, 2, (0, 0, 255), 2) for pts in auricular]

    cv2.imshow("auricular", copy)
    cv2.waitKey(0)
        





def no_finger_found(finger):
    out = ""
    fings = set([i for i in range(20)])
    finger_ = set(finger)
    
    no_finger = [fing for fing in fings if not(fing in finger_)]

    print("")
    print("")

    print(len(no_finger), no_finger)
    if len(no_finger) > 0 and no_finger[0] == 0:
        print("reply or turn \n")
        out = True
    #toujours pas le 0 et 1 :
    if len(no_finger) > 0 and no_finger[0] == 0 and no_finger[1] == 1:
        print("reply or turn 2 \n")
        out = True
    return out


def treat_skeletton_points(skeletton, position, finger, rectangle, crop):


    x, y, w, h = rectangle
    mid = int((x+w) / 2), int((y+h) / 2)

    no_fng_fnd = no_finger_found(finger)

    palm_center =  position[0][0]
    palm = [[position[5][0], position[9][0], position[13][0],
            position[17][0], position[0][0], position[0][1], position[1][1]],
            [position[5][0], position[9][0], position[13][0],
            position[17][0], position[1][1], position[0][1], position[0][0]]]

    thumb = position[1:4]
    index = position[5:8]
    major = position[9:12]
    annular = position[13:16]
    auricular = position[17:20]


    position_hand = paume(position[0][0], mid, finger)
    hand_loc = hand_location(thumb[-1], finger, mid)
    palm_analyse(hand_loc, palm_center, palm, rectangle, crop, no_fng_fnd)


    thumb_analyse(thumb, palm_center, index, rectangle, crop)
    index_analyse(index, palm_center, rectangle, crop)

    major_analyse(major, palm_center, rectangle, crop)



    #annular_analyse(annular, palm_center, rectangle, crop)
    #auricular_analyse(auricular, palm_center, rectangle, crop)












def save(crop, C):
    cv2.imwrite(r"C:\Users\jeanbaptiste\Desktop\hand_picture\a" + str(C) + ".jpg", crop)
    C += 1
    return C


C = 0

def hand(frame, detection_graph, sess, head_box):
    global C
    frame_copy = frame.copy()

    #head_hand_distance_possibility(head_box, frame)

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes, scores = detect_objects(frameRGB, detection_graph, sess)

    detections = hands_detections(scores, boxes, frame)

    for nb, hand in enumerate(detections):

        skinYCrCb, crop, copy = skin_detector(hand, frame, frame_copy)
        copy = crop.copy()

        contours = hand_treatment(skinYCrCb, crop)
        copy, rectangle = make_bitwise(contours, copy)

        C = save(copy, C)


        protoFile = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handa\models\pose_deploy.prototxt"
        weightsFile = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handa\models\pose_iter_102000.caffemodel"

        #points, position, finger = hand_skelettor(copy, protoFile, weightsFile)
        #treat_skeletton_points(points, position, finger, rectangle, crop)


    #cv2.imshow("crop_convex", frame_copy)







if __name__ == "__main__":
    

    IM = 435
    IM = 531


    image = r"C:\Users\jeanbaptiste\Desktop\hand_picture\a{}.jpg".format(str(IM))
    #image = r"C:\Users\jeanbaptiste\Desktop\hand_picture\{}.jpg".format(str(IM))

    img = cv2.imread(image)
    copy_img = img.copy()

    protoFile = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handa\models\pose_deploy.prototxt"
    weightsFile = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handa\models\pose_iter_102000.caffemodel"


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours = [sorted(cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0],
                                        key=cv2.contourArea)][0]



    copy = img.copy()
    rectangle = cv2.boundingRect(contours[-1])



    points, position, finger = hand_skelettor(copy_img, protoFile, weightsFile)
    treat_skeletton_points(points, position, finger, rectangle, img)











