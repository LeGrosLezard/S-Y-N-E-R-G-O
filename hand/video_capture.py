import cv2
import tensorflow as tf
import numpy as np
from time import time
import imutils

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
    var = 30
    hand = img[int(hand[0][2] - var):int(hand[0][3] + var), int(hand[0][0]) - var:int(hand[0][1]) + var]
    return hand

def skin_color(hand):

    min_YCrCb = np.array([0,140,85],np.uint8)
    max_YCrCb = np.array([240,180,130],np.uint8)

    imageYCrCb = cv2.cvtColor(hand,cv2.COLOR_BGR2YCR_CB)
    skinRegionYCrCb = cv2.inRange(imageYCrCb,min_YCrCb,max_YCrCb)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    skinMask = cv2.dilate(skinRegionYCrCb, kernel, iterations = 2)
    skinMask = cv2.erode(skinMask,kernel,iterations = 1)
    skinYCrCb = cv2.bitwise_and(hand, hand, mask = skinMask)

    return skinYCrCb

def video_capture(video_name, hand_model):

    detection_graph, sess = load_inference_graph(hand_model)
    video = cv2.VideoCapture(video_name)
    detections = [[], []]
    fgbg = cv2.createBackgroundSubtractorMOG2(history=10, detectShadows=False)


    while True:


        frame = cv2.resize(video.read()[1], (500, 400))

        R = cv2.RETR_TREE
        P = cv2.CHAIN_APPROX_NONE
        suba = fgbg.apply(frame)
        contours, _ = cv2.findContours(suba, R, P)
        for cnts in contours:
            if cv2.contourArea(cnts) > 300: #500 / 1.7:
                x, y, w, h = cv2.boundingRect(cnts)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3, 1)



        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes, scores = detect_objects(frameRGB, detection_graph, sess)
        for i in range(2):
            if (scores[i] > 0.10):
                (left, right, top, bottom) = (boxes[i][1] * 500, boxes[i][3] * 500,
                                              boxes[i][0] * 400, boxes[i][2] * 400)
                p1 = (int(left), int(top))
                p2 = (int(right), int(bottom))
                cv2.rectangle(frame, p1, p2, (77, 255, 9), 3, 1)











        cv2.imshow("mask", frame)


        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
