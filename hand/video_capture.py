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



def draw_box_on_image(scores, boxes):

    im_width = 500; im_height = 400

    box = [(boxes[i][1] * im_width, boxes[i][3] * im_width,
            boxes[i][0] * im_height, boxes[i][2] * im_height)
           for i in range(2) if (scores[i] > 0.20)]
    return box



def add_border(img, crop):

    height, width = img.shape[:2]
    height_crop, width_crop = crop.shape[:2]

    addHeight = int((height - height_crop) / 2)
    addWidth = int((width - width_crop) / 2)
    
    crop = cv2.copyMakeBorder(crop, addHeight, addHeight, 
                 addWidth, addWidth, cv2.BORDER_CONSTANT, value= (0, 0, 0))
    return crop


def determination_hand(detections):
    """ droite ou gauche ?"""

    hands = [[i for i in detections if (250 - i[0]) < 0], [i for i in detections if (250 - i[0]) > 0]]
    return hands[0], hands[1]



def only_part(leftHand, rightHand):
    """que le pouce par example"""
    
    def add_(hand):
        var = 40
        hand = [(hand[0][0] - var, hand[0][1] + var, hand[0][2] - var, hand[0][3] + var)]
        return hand
    
    try:
        if leftHand[0][1] - leftHand[0][0] < 40:
            leftHand = add_(leftHand)
        if rightHand[0][1] - rightHand[0][0] < 40:rightHand = add_(rightHand)

    except:
        pass

    return leftHand, rightHand


def hands(hand, img):
    
    var = 25
    hand = img[int(hand[0][2] - var):int(hand[0][3] + var), int(hand[0][0]) - var:int(hand[0][1]) + var]

    return hand




def CNN_jb(detections):
##    for i in detections:
##        print(int(i[0][0]), int(i[0][2]))
##
##    print("")
    pass


def video_capture(video_name, hand_model):

    detection_graph, sess = load_inference_graph(hand_model)
    video = cv2.VideoCapture(video_name)
    detections = []

    while True:

        frame = cv2.resize(video.read()[1], (500, 400))
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        boxes, scores = detect_objects(frameRGB, detection_graph, sess)

        areas = draw_box_on_image(scores, boxes)

        left_hand, right_hand = determination_hand(areas)
        left_hand, right_hand = only_part(left_hand, right_hand)

        try:
            left_hand = hands(left_hand, frame)
            right_hand = hands(right_hand, frame)

            cv2.rectangle(frame, (int(areas[0][0]), int(areas[0][2])), (int(areas[0][1]), int(areas[0][3])), (0,0, 255) , 3)
            cv2.rectangle(frame, (int(areas[1][0]), int(areas[1][2])), (int(areas[1][1]), int(areas[1][3])), (255, 0, 0), 3)


        except:
            CNN_jb(detections)


        if len(detections) == 20:
            detections = detections[10:]
        detections.append(areas)






        try:
        #Dsiplay
            #left_hand = add_border(frame, left_hand)
            #right_hand = add_border(frame, right_hand)

            #h,w = left_hand.shape[:2]
            #right_hand = cv2.resize(right_hand, (w, h))

            #frame = cv2.resize(frame, (w, h))
            #displaying = np.hstack((left_hand, frame))
            #displaying = np.hstack((displaying, right_hand))
            #displaying = np.hstack((left_hand, right_hand))

            cv2.imshow("tdisplaying", frame)



        except:
            pass

        if cv2.waitKey(0) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
























