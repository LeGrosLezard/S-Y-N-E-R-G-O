import cv2
import math
import time

import imutils
import numpy as np
#import tensorflow as tf
from matplotlib import pyplot as plt
from numpy import expand_dims, squeeze

from scipy.spatial import distance as dist



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



def thumb_analyse(thumb, palm, index, rectangle, crop):

    copy = crop.copy()
    cv2.circle(copy, palm, 2, (255, 255, 255), 2)
    print("")
    print("pouce")

    thumb_circle = [j for i in thumb for j in i]
    [cv2.circle(copy, pts, 2, (0, 0, 255), 2) for pts in thumb_circle]


    thumb_pts = list(set(thumb))
    for i in thumb_pts:
        if i == (0, 0):
            thumb_pts.remove(i)
    print("points:", len(thumb_pts))



    analyse_space_thumb_fingers(thumb, index, palm, crop)







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

    cv2.circle(copy, palm, 2, (255, 255, 255), 2)

    
    cv2.circle(copy, index[0][0], 2, (255, 0, 0), 2)
    cv2.circle(copy, index[1][0], 2, (0, 255, 0), 2)
    cv2.circle(copy, index[2][0], 2, (0, 0, 0), 2)
    cv2.circle(copy, index[2][1], 2, (0, 0, 255), 2)

    doigts_plié([index[0][0], index[1][0], index[2][0], index[2][1]], crop)



    phax1 = dist.euclidean(index[0][0], index[0][1])
    cv2.line(copy, index[0][0], index[0][1], (0,0,0), 1)
    length += phax1
    phalange("phalange 1", phax1, index[0][0], index[0][1])


    phax2 = dist.euclidean(index[1][0], index[1][1])
    cv2.line(copy, index[1][0], index[1][1], (0,0,0), 1)
    length += phax2
    phalange("phalange 2", phax2, index[1][0], index[1][1])

    phax3 = dist.euclidean(index[2][0], index[2][1])
    cv2.line(copy, index[2][0], index[2][1], (0,0,0), 1)
    length += phax3
    phalange("phalange 3", phax3, index[2][0], index[2][1])


    print(length)



    index = [j for i in index for j in i]
    index = list(set(index))
    for i in index:
        if i == (0, 0):
            index.remove(i)
    print("points:", len(index))




    cv2.imshow("index", copy)
    cv2.waitKey(0)


    




def major_analyse(major, palm, rectangle, crop):

    print("")
    print("major")


    copy = crop.copy()
    cv2.circle(copy, palm, 2, (255, 255, 255), 2)


    cv2.circle(copy, major[0][0], 2, (255, 0, 0), 2)
    cv2.circle(copy, major[1][0], 2, (0, 255, 0), 2)
    cv2.circle(copy, major[2][0], 2, (0, 0, 0), 2)
    cv2.circle(copy, major[2][1], 2, (0, 0, 255), 2)

    doigts_plié([major[0][0], major[1][0], major[2][0], major[2][1]], crop)


    length = 0

    phax1 = dist.euclidean(major[0][0], major[0][1])
    cv2.line(copy, major[0][0], major[0][1], (0,0,0), 1)
    length += phax1
    phalange("phalange 1", phax1, major[0][0], major[0][1])

    phax2 = dist.euclidean(major[1][0], major[1][1])
    cv2.line(copy, major[1][0], major[1][1], (0,0,0), 1)
    length += phax2
    phalange("phalange 2",phax2, major[1][0], major[1][1])

    phax3 = dist.euclidean(major[2][0], major[2][1])
    cv2.line(copy, major[2][0], major[2][1], (0,0,0), 1)
    length += phax3

    phalange("phalange 3", phax3, major[2][0], major[2][1])


    major = [j for i in major for j in i]
    major = list(set(major))
    for i in major:
        if i == (0, 0):
            major.remove(i)
    print("points:", len(major))



    cv2.imshow("major", copy)
    cv2.waitKey(0)





def annular_analyse(annular, palm, rectangle, crop):

    print("")
    print("annular")
    
    copy = crop.copy()
    cv2.circle(copy, palm, 2, (255, 255, 255), 2)


    length = 0

    phax1 = dist.euclidean(annular[0][0], annular[0][1])
    cv2.line(copy, annular[0][0], annular[0][1], (0,0,0), 1)
    length += phax1
    phalange("phalange 1", phax1, annular[0][0], annular[0][1])

    phax2 = dist.euclidean(annular[1][0], annular[1][1])
    cv2.line(copy, annular[1][0], annular[1][1], (0,0,0), 1)
    length += phax2
    phalange("phalange 2",phax2, annular[1][0], annular[1][1])

    phax3 = dist.euclidean(annular[2][0], annular[2][1])
    cv2.line(copy, annular[2][0], annular[2][1], (0,0,0), 1)
    length += phax3

    phalange("phalange 3", phax3, annular[2][0], annular[2][1])




    annular = [j for i in annular for j in i]
    [cv2.circle(copy, pts, 2, (0, 0, 255), 2) for pts in annular]


    annular = list(set(annular))
    for i in annular:
        if i == (0, 0):
            annular.remove(i)
    print("points:", len(annular))



    cv2.imshow("annular", copy)
    cv2.waitKey(0)
    



def auricular_analyse(auricular, palm, rectangle, crop):

    print("")
    print("auricular")
    
    copy = crop.copy()
    cv2.circle(copy, palm, 2, (255, 255, 255), 2)

    auricular = [j for i in auricular for j in i]
    [cv2.circle(copy, pts, 2, (0, 0, 255), 2) for pts in auricular]

    auricular = list(set(auricular))
    for i in auricular:
        if i == (0, 0):
            auricular.remove(i)
    print("points:", len(auricular))



    cv2.imshow("auricular", copy)
    cv2.waitKey(0)
        


def sign(pouce, index):
    if abs(pouce[-1][1][0] - index[-1][1][0]) <= 10 and\
       abs(pouce[-1][1][1] - index[-1][1][1]) <= 10:
        print("index pouce rond")





def reorganize_finger(thumb, index, major, annular, auricular, hand_localisation, crop):

    copy = crop.copy()

    #sommets doigts
    end_fingers = [[j for i in index for j in i if j != (0, 0)],
                   [j for i in major for j in i if j != (0, 0)],
                   [j for i in annular for j in i if j != (0, 0)],
                   [j for i in auricular for j in i if j != (0, 0)]]

    thumb_end = [j for i in thumb for j in i if j != (0, 0)][-1]
    cv2.circle(copy, thumb_end, 2, (0, 0, 255), 2)

    [cv2.circle(copy, fingers[-1], 2, (255, 0, 0), 2) for fingers in end_fingers]
    end_fingers = [fingers[-1] for fingers in end_fingers]


    repear_finger = []
    thumb_fingers_points = []
    #on récupere la distance entre le pouce et les doigts
    #ensuite on va devoir sort les distance.
    #donc pour s'y retrouver on fait un repear_finger avec:
        #les coordonées du sommet des doigts mais aussi la distance
    for finger in end_fingers:
        cv2.line(copy, thumb_end, finger, (0, 255, 0), 1)
        distance = dist.euclidean(thumb_end, finger)
        thumb_fingers_points.append(distance)
        repear_finger.append((distance, finger))

    thumb_fingers_points = sorted(thumb_fingers_points)
    #print(thumb_fingers_points)
    #print(repear_finger)

    finger_sorted = [thumb]
    all_finger = [thumb, index, major, annular, auricular]
    #on compare les distances sorted avec le repaire.
    for i in thumb_fingers_points:
        for j in repear_finger:
            if i == j[0]:
                #on compare le repaire avec les points du skelette.
                for k in all_finger:
                    if j[1] == (k[-1][1]):
                        finger_sorted.append(k)


    #print(finger_sorted)


##    copy2 = crop.copy()
##    for i in finger_sorted:
##        for j in i:
##            for k in j:
##                cv2.circle(copy2, k, 2, (255, 0, 0), 2)
##
##        cv2.imshow("copy2", copy2)
##        cv2.waitKey(0)


    thumb = finger_sorted[0]
    index = finger_sorted[1]
    major = finger_sorted[2]
    annular = finger_sorted[3]
    auricular = finger_sorted[4]


    cv2.imshow("reorganisation", copy)
    cv2.waitKey(0)

    return thumb, index, major, annular, auricular




def palm_analyse(hand_localised, palm_center, palm, rectangle, crop):

    copy = crop.copy()

    if hand_localised == "pouce droite": area = palm[0]
    else: area = palm[1]

    palm_area = np.array([(pts[0], pts[1]) for pts in area if pts != (0, 0)])
    cv2.drawContours(copy, [palm_area], 0, (0, 255, 0), 1)
    palm_area = cv2.contourArea(palm_area)

    if palm_area < 300: print("peut etre main non tournée paume et on peut definir la main", palm_area)
    elif palm_area > 300: print("main tournée paume  et on peut definir la main", palm_area)

    cv2.circle(copy, palm_center, 2, (255, 255, 255), 1)
    [cv2.circle(copy, pts, 2, (0, 0, 0), 1) for pts in area]

    cv2.imshow("palm", copy)
    cv2.waitKey(0)


def hand_location(thumb, index, major, annular, auricular, crop):

    hand = ""
    copy = crop.copy()

    end_fingers = [[j for i in index for j in i if j != (0, 0)],
                   [j for i in major for j in i if j != (0, 0)],
                   [j for i in annular for j in i if j != (0, 0)],
                   [j for i in auricular for j in i if j != (0, 0)]]

    end_fingers = [fingers[-1] for fingers in end_fingers]
    [cv2.circle(copy, fingers, 2, (255, 0, 0), 2) for fingers in end_fingers]

    thumb = [j for i in thumb for j in i if j != (0, 0)][-1]
    cv2.circle(copy, thumb, 2, (0, 0, 255), 2)

    left = 0
    right = 0
    for fing in end_fingers:
        if thumb[0] < fing[0]:
            left += 1
        elif thumb[0] > fing[0]:
            right += 1

    if left > right:
        hand = "pouce gauche"
    elif right > left:
        hand = "pouce droite"
    else:
        print("probleme HAND LOCATION")

    cv2.imshow("Hand", copy)
    cv2.waitKey(0)

    print(hand)
    return hand



def reorganize_finger_position(thumb, index, major, annular, auricular, crop):
    copy = crop.copy()

    fingers = [ [j for i in thumb for j in i if j != (0, 0)],
                [j for i in index for j in i if j != (0, 0)],
                [j for i in major for j in i if j != (0, 0)],
                [j for i in annular for j in i if j != (0, 0)],
                [j for i in auricular for j in i if j != (0, 0)]]


    #display
    fingers = [list(set(i)) for i in fingers]
    for i in fingers:
        copy = crop.copy()
        print(i)
        for j in i:
            cv2.circle(copy, j, 2, (0, 0, 255), 2)
            cv2.imshow("copy", copy)
            cv2.waitKey(0)

    #on verifie chaques doigts et essayons de detecter un doigt détecter plusieurs fois
    for i in range(len(fingers)):
        if i + 1 < len(fingers):
            print(fingers[i])
            print(fingers[i+1])


            for j in fingers[i]:
                for k in fingers[i + 1]:
                    if abs(j[0] - k[0]) < 10 and\
                       abs(j[1] - k[1]) < 10:
                        print("deux fois le meme doigt ?")


    #MAIS avant la prochaine étape faut remettre les points dans un ordre croissant, décroissant
        #MAIS on ne peut toujours pas savoir si la main et vers le bas ou vers le haut...
                        #donc croissant miam




    #on essais de voir si un pts de ce doigt et allé sur un autre doigt
    for i in fingers:
        print(i)
        for j in range(len(i)):
            if j + 1 < len(i):

                a = dist.euclidean(i[j], i[j + 1])
                print(a)

        print("")

    cv2.imshow("finger_verification", copy)
    cv2.waitKey(0)





def treat_skeletton_points(skeletton, position, finger, proba, rectangle, crop):


    x, y, w, h = rectangle

    palm_center =  position[0][0]

    palm = [[position[5][0], position[9][0], position[13][0],
             position[17][0], position[0][1], position[1][1]],

            [position[5][0], position[9][0], position[13][0],
             position[17][0], position[0][1], position[1][1]]]

    thumb = position[1:4]
    index = position[5:8]
    major = position[9:12]
    annular = position[13:16]
    auricular = position[17:20]


    hand_localised = hand_location(thumb, index, major, annular, auricular, crop)
    #palm_analyse(hand_localised, palm_center, palm, rectangle, crop)

    thumb, index, major, annular, auricular =\
    reorganize_finger(thumb, index, major, annular, auricular, hand_localised, crop)

    finger_verification(thumb, index, major, annular, auricular, crop)





    #thumb_analyse(thumb, palm_center, index, rectangle, crop)
    #index_analyse(index, palm_center, rectangle, crop)

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
    

    IM = 67 #g
    IM = 83 #d 186
    IM = 27 #g area 538










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





#TODO
    #detecter pouce et annulaire
    #si pouce auriculaire .. index => auri -> index - > pliéq
    #changement de perspective doigt plus long -> penché vers torse et versa #531
    #angle entre debut doigt et fin ex 259 doigt coté face
    #angle 261
    #pouce via index via majeur ect ex pouce rond index -> 261
    #plusieurs main pouce rond, ok, rien et circularité genre ca tourne rond
    #verifier hnad reoganization si pas tous les doigts pas pouce
    #main retourner du coup devient gauche -> droite et vis versa




