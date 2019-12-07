import cv2
import tensorflow as tf
import numpy as np
from time import time


print(tf.version.VERSION)


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

    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    image_np_expanded = np.expand_dims(image_np, axis=0)

    (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores,
                                             detection_classes, num_detections],
                                             feed_dict={image_tensor: image_np_expanded})

    return np.squeeze(boxes), np.squeeze(scores)


 
def recuperate_detection(scores, boxes):

    width = 500; height = 400

    box = [(boxes[i][1] * width, boxes[i][3] * width,
            boxes[i][0] * height, boxes[i][2] * height)
           for i in range(2) if (scores[i] > 0.20)]

    return box


def determination_hand(detections):
    """ droite ou gauche ?"""
    hands = [[i for i in detections if (250 - i[0]) < 0], [i for i in detections if (250 - i[0]) > 0]]
    return hands[0], hands[1]


def only_part(hand, detections):
    """que le pouce par example"""
    if hand[0][1] - hand[0][0] < 40:
        hand = [( detections[0][0],detections[0][1], detections[0][2], detections[0][3])]
    return hand


def no_hand(detections, hand):
    hand = [( detections[0][0],detections[0][1], detections[0][2], detections[0][3])]
    return hand


def hands(hand, img):
    """Make a crop"""
    var = 25
    hand = img[int(hand[0][2] - var):int(hand[0][3] + var), int(hand[0][0]) - var:int(hand[0][1]) + var]
    return hand

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

    detection_graph, sess = load_inference_graph(hand_model)
    video = cv2.VideoCapture(video_name)
    detections = [[], []]
    fgbg = cv2.createBackgroundSubtractorMOG2()


    while True:



        frame = cv2.resize(video.read()[1], (500, 400))
        copy = frame.copy()
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        fgmask = fgbg.apply(frame)
        bg = cv2.bitwise_and(frame, frame, mask=fgmask)

        cv2.imshow("bg", bg)

        frameRGB = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
        bg = skin_color(bg)

        gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
        contours = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

        cv2.drawContours(copy, contours, -1, (255, 255, 255), 1)
        cv2.fillPoly(copy, pts =contours, color=(255, 255, 255))

        gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(gray, 250, 255,cv2.THRESH_BINARY)


        contours = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
        for i in contours:
            if cv2.contourArea(i) > 100:
                x, y, w, h = cv2.boundingRect(i)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)



        cv2.imshow("fgmask", frame)




































##        #Detect 2 boxes with > 0.27
##        boxes, scores = detect_objects(frameRGB, detection_graph, sess)
##
##        #Recuperate 2 boxes
##        areas = recuperate_detection(scores, boxes)
##        #Define left and right hands
##        left_hand, right_hand = determination_hand(areas)
##
##        #No hand
##        if left_hand == []:left_hand = no_hand(detections[0], "left")
##        if right_hand == []:right_hand = no_hand(detections[1], "right")
##
##        #Litlle detection
##        left_hand = only_part(left_hand, detections[0])
##        right_hand = only_part(right_hand, detections[1])
##
##        detections[0] = left_hand
##        detections[1] = right_hand
##
##        cv2.rectangle(frame, (int(right_hand[0][0]), int(right_hand[0][2])), (int(right_hand[0][1]), int(right_hand[0][3])), (255, 0, 0), 3)
##        cv2.rectangle(frame, (int(left_hand[0][0]), int(left_hand[0][2])),(int(left_hand[0][1]), int(left_hand[0][3])), (0,0, 255) , 3)
##
##        #Croping
##        left_hand = hands(left_hand, frame)
##        right_hand = hands(right_hand, frame)
##
##        left_hand_skin = skin_color(left_hand)
##        right_hand_skin = skin_color(right_hand)
##        frame_skin = skin_color(frame)
##
##
##
##
##
##
##        cv2.imshow("left_hand_skin", left_hand_skin)
##
##        cv2.imshow("right_hand_skin", right_hand_skin)
##        cv2.imshow("frame_skin", frame_skin)
##
##
##        cv2.imshow("frame", frameRGB)


        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
























