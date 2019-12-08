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

    droite = []
    gauche = []

    hist_droite = [[], []]
    hist_gauche = [[], []]
    while True:

        liste = []
        possible_droite = ""
        possible_gauche = ""


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


        print("")
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes, scores = detect_objects(frameRGB, detection_graph, sess)
        for i in range(2):
            if (scores[i] > 0.10):
                (left, right, top, bottom) = (boxes[i][1] * 500, boxes[i][3] * 500,
                                              boxes[i][0] * 400, boxes[i][2] * 400)
                p1 = (int(left), int(top))
                p2 = (int(right), int(bottom))


                if p1[0] < 250:
                    droite.append((p1[0], p1[1], p2[0], p2[1]))
                    hist_droite[0].append(p1[0])
                    hist_droite[1].append(p1[1])

                    print("droite")
                    try:
                        print(hist_droite[0][-1], (hist_droite[0][-2]))
                    except:pass
                    try:
                        
##                        print(hist_droite[0][-1] - hist_droite[0][-2],
##                              hist_droite[1][-1] - hist_droite[1][-2])

                        if abs(hist_droite[0][-1] - hist_droite[0][-2]) > 50 or\
                           abs(hist_droite[1][-1] - hist_droite[1][-2]) > 50:
                            possible_droite = "impossible"
                            print(possible_droite)
                            if possible_droite == "impossible":
                                droite.remove(droite[-1])
                                hist_droite[0].remove(hist_droite[-1])
                                hist_droite[1].remove(hist_droite[-1])
 
                        else:
                            print("possible droite")

                    except:pass



                else:
                    gauche.append((p1[0], p1[1], p2[0], p2[1]))
                    hist_gauche[0].append(p1[0])
                    hist_gauche[1].append(p1[1])

                    print("")

                    print("gauche")
                    try:
                        print(hist_gauche[0][-1], (hist_gauche[0][-2]))
                    except:pass
                    try:

                        if abs(hist_gauche[0][-1] - hist_gauche[0][-2]) > 50 or\
                           abs(hist_gauche[1][-1] - hist_gauche[1][-2]) > 50:
                            possible_gauche = "impossible"
                            print(possible_gauche)
                            if possible_gauche == "impossible":
                                gauche.remove(gauche[-1])
                                hist_gauche[0].remove(hist_gauche[-1])
                                hist_gauche[1].remove(hist_gauche[-1])
                        else:

                            print("possible gauche")

                    except:pass


        print("")
        print("")
        print("")
        print("")
        try:
            nb = 80
            droite_points = [[], [], [], []]
            for i in liste:
                #print(i)
                a = abs(i[0] - droite[0][0])
                b = abs(i[1] - droite[0][1])
                c = abs(i[2] - droite[0][2])
                d = abs(i[3] - droite[0][3])
                #print("droite", a, b, c, d)
                if a < nb and b < nb and c < nb and d < nb:
                    droite_points[0].append(i[0])
                    droite_points[1].append(i[1])
                    droite_points[2].append(i[2])
                    droite_points[3].append(i[3])
                    #print("droite oui")


            print("")
            gauche_points = [[], [], [], []]
            for i in liste:
                #print(i)
                a = abs(i[0] - gauche[0][0])
                b = abs(i[1] - gauche[0][1])
                c = abs(i[2] - gauche[0][2])
                d = abs(i[3] - gauche[0][3])
                #print("gauche", a, b, c, d)
                if a < nb and b < nb and c < nb and d < nb:
                    gauche_points[0].append(i[0])
                    gauche_points[1].append(i[1])
                    gauche_points[2].append(i[2])
                    gauche_points[3].append(i[3])
                    #print("gauche oui")


            if len(droite_points[0]) != 0:
                cv2.rectangle(frame, (min(droite_points[0]), min(droite_points[1])),
                                     (max(droite_points[2]), max(droite_points[3])), (77, 0, 0), 3, 1)

            if len(droite) == 1 and len(droite_points[0]) != 0:

                droite.append((min(droite_points[0]), min(droite_points[1]),
                               max(droite_points[2]), max(droite_points[3])))

                hist_droite[0].append(min(droite_points[0]))
                hist_droite[1].append(min(droite_points[1]))

            elif len(droite) == 2 and len(droite_points[0]) != 0:
                fusion_droite = [[], [], [], []]

                for i in range(4):
                    fusion_droite[i].append(droite[-1][i])

                for nb, i in enumerate(droite_points):
                    for j in i:
                        fusion_droite[nb].append(j)
                    

                droite[-1] = (min(fusion_droite[0]), min(fusion_droite[1]),
                              max(fusion_droite[2]), max(fusion_droite[3]))



            if possible_droite == "impossible" and len(droite_points[0]) != 0:
                droite[-1] = ((min(droite_points[0]), min(droite_points[1]),
                               max(droite_points[2]), max(droite_points[3])))








            if len(gauche_points[0]) != 0:
                cv2.rectangle(frame, (min(gauche_points[0]), min(gauche_points[1])),
                                     (max(gauche_points[2]), max(gauche_points[3])), (77, 0, 0), 3, 1)

            if len(gauche) == 1 and len(gauche_points[0]) != 0:

                gauche.append((min(gauche_points[0]), min(gauche_points[1]),
                              max(gauche_points[2]), max(gauche_points[3])))

                hist_gauche[0].append(min(gauche_points[0]))
                hist_gauche[1].append(min(gauche_points[1]))


            elif len(gauche) == 2 and len(gauche_points[0]) != 0:
                fusion_gauche = [[], [], [], []]


                for i in range(4):
                    fusion_gauche[i].append(gauche[-1][i])

                for nb, i in enumerate(gauche_points):
                    for j in i:
                        fusion_gauche[nb].append(j)

                gauche[-1] = (min(fusion_gauche[0]), min(fusion_gauche[1]),
                              max(fusion_gauche[2]), max(fusion_gauche[3]))


            if possible_gauche == "impossible" and len(gauche_points[0]) != 0:
                gauche[-1] = ((min(droite_points[0]), min(droite_points[1]),
                               max(droite_points[2]), max(droite_points[3])))




            if len(droite) == 3:
                a = droite[0][0] - droite[1][0]
                b = droite[0][0] -  droite[2][0]
                if a < b:
                    droite[-1] = droite[-2]

            if len(gauche) == 3:
                a = gauche[0][0] - gauche[1][0]
                b = gauche[0][0] -  gauche[2][0]
                if a < b:
                    gauche[-1] = gauche[-2]

            print("")
            print("")


            cv2.rectangle(frame, (droite[-1][0], droite[-1][1]),
                          (droite[-1][2], droite[-1][3]), (77, 255, 9), 3)

            cv2.rectangle(frame, (gauche[-1][0], gauche[-1][1]),
                          (gauche[-1][2], gauche[-1][3]), (77, 255, 9), 3)




            droite = [droite[-1]]
            gauche = [gauche[-1]]
        

        except:
            pass









        cv2.imshow("mask", frame)


        if cv2.waitKey(0) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
