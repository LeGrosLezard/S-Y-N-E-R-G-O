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


def fusion():

    pass


def video_capture(video_name, hand_model):

    detection_graph, sess = load_inference_graph(hand_model)
    video = cv2.VideoCapture(video_name)
    detections = [[], []]
    fgbg = cv2.createBackgroundSubtractorMOG2(history=10, detectShadows=False)

    last = []
    while True:

        liste = []
        frame = cv2.resize(video.read()[1], (500, 400))

        R = cv2.RETR_TREE
        P = cv2.CHAIN_APPROX_NONE
        suba = fgbg.apply(frame)
        contours, _ = cv2.findContours(suba, R, P)
        for cnts in contours:
            if 1000 > cv2.contourArea(cnts) > 250: #500 / 1.7:
                x, y, w, h = cv2.boundingRect(cnts)
                liste.append((x, y, x+w, y+h))
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
                last.append((p1[0], p1[1], p2[0], p2[1]))


        for i in liste:
            print(i)

        ok = [[], [], [], []]
        for i in liste:
            a = abs(i[0] - last[1][0])
            b = abs(i[1] - last[1][1])
            c = abs(i[2] - last[1][2])
            d = abs(i[3] - last[1][3])

            print(a, b ,c ,d, "1")

            nb = 100;
            if a < nb and b < nb and c < nb and d < nb:
                ok[0].append(i[0])
                ok[1].append(i[1])
                ok[2].append(i[2])
                ok[3].append(i[3])
                print("ouiiiiiiii")
        

        ok1 = [[], [], [], []]
        for i in liste:
            a = abs(i[0] - last[0][0])
            b = abs(i[1] - last[0][1])
            c = abs(i[2] - last[0][2])
            d = abs(i[3] - last[0][3])
            print(a, b ,c ,d, "2")

            if a < nb and b < nb and c < nb and d < nb:
                ok1[0].append(i[0])
                ok1[1].append(i[1])
                ok1[2].append(i[2])
                ok1[3].append(i[3])
                print("oui")

        if len(ok[0]) != 0:
            cv2.rectangle(frame, (min(ok[0]), min(ok[1])), (max(ok[2]), max(ok[3])), (77, 0, 0), 3, 1)
        if len(ok1[0]) != 0:
            cv2.rectangle(frame, (min(ok1[0]), min(ok1[1])), (max(ok1[2]), max(ok1[3])), (77, 0, 0), 3, 1)

        print("")
        print("actuel", last[-2], last[-1])
        print("passé", last[0], last[1])
        print("")

        print("current last", last)

        last = [last[-2], last[-1]]


        cv2.imshow("mask", frame)


        if cv2.waitKey(0) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
