import cv2
import math
import time

import imutils
import numpy as np
#import tensorflow as tf
from matplotlib import pyplot as plt
from numpy import expand_dims, squeeze

from scipy.spatial import distance as dist


from palm_analyse import palm_analyse
from no_finger_found import no_finger_found
from reorganize_finger import reorganize_finger
from reorganize_phax_position import reorganize_phax_position
from hand_location import hand_location
from skeletton import hand_skelettor
from hand_mask import skin_detector, hand_treatment, make_bitwise
from sign import sign
from identify_fingers import identify_fingers



def save(crop, C):
    cv2.imwrite(r"C:\Users\jeanbaptiste\Desktop\hand_picture\a" + str(C) + ".jpg", crop)
    C += 1
    return C

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





def treat_skeletton_points(skeletton, position, finger, proba, rectangle, crop):


    x, y, w, h = rectangle
    print("Box de la main est de :", rectangle)


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

    miss_points = no_finger_found(finger, thumb, index, major, annular, auricular)

    #location of the thumb
    hand_localised = hand_location(thumb, index, major, annular, auricular, crop)

    #area of the palm
    fingers_direction = palm_analyse(hand_localised, palm_center, palm, rectangle, crop,
                                     thumb, index, major, annular, auricular)



    #delete false points finger detection
    sorted_fingers, fingers_orientation = reorganize_phax_position(thumb, index, major, annular,
                                             auricular, crop, fingers_direction)

    #reorganize finger's position
    thumb, sorted_points,\
    direction , axis = reorganize_finger(crop, miss_points,
                                         sorted_fingers, fingers_orientation)


    identify_fingers(thumb, sorted_points, crop, rectangle, direction, axis)

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










C = 626

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
    


    IM = 55


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
    #7 No pouce
    #3 annuiare
    #paume de la main




#FUNCTION
    #rangement des pts du doigt -> 77
    #egalité réglé 1
    #delete phax 17; 25; 27; 5; 26; 29; 45
    #reorganisation doigt 23; 25 (pts theorique non respecté)
    #finger remove 27; 25;29;35      
    #Identify finger 27; 25
    #last reorganise 49
    #extremum phax 55






















    






