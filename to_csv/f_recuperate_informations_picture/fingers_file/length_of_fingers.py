import cv2
import math
from scipy.spatial import distance as dist


#============================================================== length_of_fingers()
def length_of_fingers(fingers_dico, crop):


    phax_dico = {"thumb": [], "I": [], "M": [], "An": [], "a": []}

    total_length = 0
    for finger_name, points in fingers_dico.items():
        for nb_pts in range(len(points)):
            if nb_pts < len(points) - 1:
                distance = dist.euclidean(points[nb_pts], points[nb_pts + 1])
                phax_dico[finger_name].append(distance)
                total_length += distance
     
        phax_dico[finger_name].append(total_length)
        total_length = 0

    for k, v in phax_dico.items():
        copy = crop.copy()
        [cv2.circle(copy, points, 2, (0, 0, 255), 2) for points in fingers_dico[k]]

        [cv2.line(copy, fingers_dico[k][nb], fingers_dico[k][nb + 1], (0, 255, 255), 2)
        for nb in range(len(fingers_dico[k])) if nb < len(fingers_dico[k]) - 1]


        print(k, v)

        cv2.imshow("copy", copy)
        cv2.waitKey(0)

    print("")
