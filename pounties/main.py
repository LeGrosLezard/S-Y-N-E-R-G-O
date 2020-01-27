import cv2

from hands.hand_detection.hand_detection import load_inference_graph
from hands.hand_treatment.skeletton.skeletton import hand_skelettor

from main_utils import hand_dection_part
from main_utils import hand_isolation_part
from main_utils import treat_skeletton_points

from main_utils import retreatement_points

from data.collect_points import collect_points


path_to_ckpt = r"C:\Users\jeanbaptiste\Desktop\frozen_inference_graph.pb"
protoFile = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handa\models\pose_deploy.prototxt"
weightsFile = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handa\models\pose_iter_102000.caffemodel"


detection_graph, sess = load_inference_graph(path_to_ckpt)



#raise
import os
liste_video = os.listdir(r"C:\Users\jeanbaptiste\Desktop\pounties\videos")
for video in liste_video:
#raise

    cap = cv2.VideoCapture("videos/{}".format(video))

    nb = 2
    c = 0
    while True:

        _, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detections, frame_copy = hand_dection_part(frame, detection_graph, sess)

        for nb, hand in enumerate(detections):

            hand_masked, rectangle = hand_isolation_part(hand, frame, frame_copy)

            points, position, finger = hand_skelettor(hand_masked, protoFile, weightsFile)

            try:

                if len(points) >= 20 and len(finger) >= 20:
                    palm_center, points_sorted = treat_skeletton_points(points, position, finger,
                                                                        rectangle, hand_masked)

                    reorganize_by_pair = retreatement_points(palm_center, points_sorted)

                    if len(reorganize_by_pair) >= 20:
                        collect_points(position, rectangle)

                    else:
                        print("reconstruction to doo mais faut mettre des (0, 0) ou on efface")


                else:
                    print("TODOOOOOOOOOOOOOOOO")
                    #collect_points THEORIQUE(points, rectangle)

            #raise
            except:
                path = r"C:\Users\jeanbaptiste\Desktop\pounties\data\error\{}.jpg"
                picture = str(c) + ".jpg"
                cv2.imwrite(path.format(picture), crop)

                c += 1


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

























