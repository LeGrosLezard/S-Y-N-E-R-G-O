import cv2
import math
from scipy.spatial import distance as dist


def similar_points_finger(fingers_dico, crop):

    copy = crop.copy()

    same = False

    for k, v in fingers_dico.items():
        for k1, v1 in fingers_dico.items():

            for i in v:
                for j in v1:

                    if i[0] + 2 > j[0] > i[0] - 2 and i[1] + 2 > j[1] > i[1] - 2 and k != k1 or\
                       j[0] + 2 > i[0] > j[0] - 2 and j[1] + 2 > i[1] > j[1] - 2 and k != k1:
                        print(k, k1)
                        same = True


    if same is False:
        print("no finger same points")
