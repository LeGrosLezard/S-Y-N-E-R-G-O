import cv2
import math
import time

import imutils
import numpy as np
#import tensorflow as tf
from matplotlib import pyplot as plt
from numpy import expand_dims, squeeze

from scipy.spatial import distance as dist

from hand_treatment import *

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

    return contours


def make_bitwise(contours, crop):

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    mask = np.zeros_like(gray)
    cv2.fillPoly(mask, [contours[-2]], 255)
    crop = cv2.bitwise_and(crop, crop, mask=mask)

    x, y, w, h = cv2.boundingRect(contours[-2])

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
    proba = []
    for i in range(22):
        # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]
        probMap = cv2.resize(probMap, (frameWidth, frameHeight))

        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        if prob > threshold :
            points.append((int(point[0]), int(point[1])))
            proba.append(prob)
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
    return skeletton, position, finger, proba



def draw(finger, position, crop, color):
    finger = [j for i in position for j in i]
    [cv2.circle(crop, pts, 2, color, -1) for pts in finger]


def phalange(pha, phax, pts1, pts2):

    if phax > 0:
        print("pahalange")
        print(phax)

    if 0 < phax < 10:
        print(pha + " pliée")

    elif phax > 0:
        direction_top = pts1[1] - pts2[1]

        if direction_top > 0:
            print(pha + " vers le haut")
        else:
            print(pha + " vers le bas")

        direction_bot = pts1[0] - pts2[0]

        if direction_bot > 5:
            print("vers droite")
        elif direction_bot < -5:
            print("vers gauche")
        else:
            print("droit")

    print("")




def doigts_plié(points, crop):

    copy = crop.copy()

    cv2.line(copy, points[0], points[1], (0, 0, 255), 2)
    cv2.line(copy, points[1], points[3], (0, 0, 255), 2)
    cv2.line(copy, points[3], points[0], (0, 0, 255), 2)
    #0 1 3 -> phalange


    #pts 3 > pts1
    if points[3][1] + 5 >= points[1][1]:
        print("doigt plié vers le bas")

    #pts3 LEFT pts0; pts3 > pts1
    if points[0][0] >= points[3][0] and points[3][1] + 5 >= points[1][1]:
        print("plié vers droit")

    #pts3 RIGHT pts0; pts3 > pts1
    if points[0][0] <= points[3][0] and points[3][1] + 5 >= points[1][1]:
        print("plié vers gauche") 

    #pts0 LEFT pts3; pts3 > pts1; (pts3 - pts0) < 15
    if points[0][0] >= points[3][0] and points[3][1] + 5 >= points[1][1] and\
       abs(points[3][1] - points[0][1]) <= 15:
        print("plié vers droit")
 
    if points[0][0] <= points[3][0] and points[3][1] + 5 >= points[1][1] and\
       abs(points[3][1] - points[0][1]) <= 15:
        print("plié vers gauche") 


    cv2.imshow("angle doigt plié", copy)
    cv2.waitKey(0)


def analyse_space_thumb_fingers(finger, finger2, palm, crop):

    copy = crop.copy()


    print(finger)
    print(finger2)

    cv2.line(copy, palm, finger[-1][1], (0,255,255), 1)
    cv2.line(copy, finger[-1][1], finger2[-1][1], (0,255,255), 1)
    cv2.line(copy, finger2[-1][1], palm, (0,255,255), 1)


    cv2.circle(copy, palm, 2, (255, 255, 255), 2)
    cv2.circle(copy, finger[-1][1], 2, (255, 255, 255), 2)
    cv2.circle(copy, finger2[-1][1], 2, (255, 255, 255), 2)


    bc = dist.euclidean(finger[-1][1], finger2[-1][1])
    ca = dist.euclidean(finger2[-1][1], palm)
    print(ab, bc, ca)

    font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    cv2.putText(copy, 'A', palm, font,  
                       1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(copy, 'B', finger[-1][1], font,  
                       1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(copy, 'C', finger2[-1][1], font,  
                       1, (255, 255, 255), 1, cv2.LINE_AA)



    #pouce plus haut qu'index
    if finger[-1][1][1] + 5 < finger2[-1][1][1]:
        print("iciiiiiiiiiii a faire")



    #pouce plus bas index
    elif finger2[-1][1][1] + 5 > finger2[-1][1][1]:

        cb_2 = (ca**2) + (ab**2) - (bc**2)
        cos = (2 * ca * ab)
        angle = math.degrees(math.acos(cb_2 / cos))
        print(angle)




    cv2.imshow("analyse space", copy)
    cv2.waitKey(0)





def index_analyse(thumb, index, major, crop):

    print("")
    print("index")

    copy = crop.copy()
    


    cv2.imshow("index", copy)
    cv2.waitKey(0)
    


def sign(pouce, index):
    try:
        if abs(pouce[-1][1][0] - index[-1][1][0]) <= 10 and\
           abs(pouce[-1][1][1] - index[-1][1][1]) <= 10:
            print("index pouce rond")
    except:
        print("ERROR SIGN")





def orientation_finger(finger):
    pass

def thumb_analyse(palm, thumb, index, crop):

    print("")
    print("pouce")

    copy = crop.copy()

    cv2.circle(copy, palm, 2, (0, 0, 255), 2)
    print(palm)

    print(thumb)
    for i in thumb:
        cv2.circle(copy, i, 2, (0, 0, 255), 2)


    #analyse_space_thumb_fingers(finger, finger2, palm, crop)

    cv2.imshow("thumb", copy)
    cv2.waitKey(0)




def treat_skeletton_points(skeletton, position, finger, proba, rectangle, crop):


    x, y, w, h = rectangle

    palm_center =  position[0][0]

    palm = [[position[5][0], position[9][0], position[13][0],
             position[17][0], position[0][1]],

            [position[5][0], position[9][0], position[13][0],
             position[17][0], position[0][1]]]

    #attribuate finger's to their initial detection
    thumb = position[1:4]
    index = position[5:8]
    major = position[9:12]
    annular = position[13:16]
    auricular = position[17:20]

    no_finger_found(finger, thumb, index, major, annular, auricular)

    #location of the thumb
    hand_localised = hand_location(thumb, index, major, annular, auricular, crop)

    #area of the palm
    fingers_direction = palm_analyse(hand_localised, palm_center, palm, rectangle, crop,
                                     thumb, index, major, annular, auricular)

    #attribuate by x axis fingers
    thumb, index, major, annular, auricular =\
    reorganize_finger(thumb, index, major, annular, auricular, hand_localised, crop)

    #delete false points finger detection
    finger_sorted = reorganize_finger_position(thumb, index, major, annular,
                                               auricular, crop, fingers_direction)

    #reattribuate points
    thumb = finger_sorted[0]
    index = finger_sorted[1]
    major = finger_sorted[2]
    annular = finger_sorted[3]
    auricular = finger_sorted[4]



    #thumb_analyse(palm_center, thumb, index, crop)
    #index_analyse(thumb, index, major, crop)

    #major_analyse(major, palm_center, rectangle, crop)

    #annular_analyse(annular, palm_center, rectangle, crop)
    #auricular_analyse(auricular, palm_center, rectangle, crop)




    sign(thumb, index)







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
    

    IM = 17






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



    points, position, finger, proba = hand_skelettor(copy_img, protoFile, weightsFile)
    treat_skeletton_points(points, position, finger, proba, rectangle, img)



#FIXED
    #mains avec tous les doigts 5 doigts visibles semblent ok





#TODO
    #image 5 un pec change major et le doigt dapres
    #changement de perspective doigt plus long -> penché vers torse et versa #531
    #angle entre debut doigt et fin ex 259 doigt coté face
    #angle 261
    #pouce via index via majeur ect ex pouce rond index -> 261


#FUNCTION
    #rangement des pts du doigt -> 77
    #egalité réglé 1
    #delete points 17

















