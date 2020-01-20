import cv2
from scipy.spatial import distance as dist
import numpy as np

#=========================================================================================== delete_finger()
def to_removing_finger(to_remove, sorted_fingers, fingers_orientation):
    
    if len(to_remove) > 0:
        print("element a supprimer :", to_remove)

        elements_finger = []
        elements_orientation = []

        for i in to_remove:
            elements_finger.append(sorted_fingers[i])
            elements_orientation.append(fingers_orientation[i])

        for i in elements_finger:
            for j in sorted_fingers:
                if i == j:
                    sorted_fingers.remove(j)
        
        for i in elements_orientation:
            for j in fingers_orientation:
                if i == j:
                    fingers_orientation.remove(j)

    print(sorted_fingers)
    print(fingers_orientation)
    print("")

    return sorted_fingers, fingers_orientation


def delete_finger(sorted_fingers, fingers_orientation, crop):

    print("DELETE FINGER")
    print(sorted_fingers, "\n")
    to_remove = []

    for i in range(len(sorted_fingers)):

        same_points_localisation = 0
        copy_delete = crop.copy()

        if i < len(sorted_fingers) - 1:

            #Draw
            [cv2.circle(copy_delete, j, 2, (255, 0, 0), 2) for j in sorted_fingers[i]]
            [cv2.circle(copy_delete, j, 2, (0, 0, 255), 2) for j in sorted_fingers[i + 1]]


            #Distance
            for j in sorted_fingers[i]:
                for k in sorted_fingers[i + 1]:

                    if abs(j[0] - k[0]) <= 12 and abs(j[1] - k[1]) <= 10 or\
                       abs(j[0] - k[0]) <= 10 and abs(j[1] - k[1]) <= 12:
                        same_points_localisation += 1


            length1 = len(sorted_fingers[i])
            length2 = len(sorted_fingers[i + 1])

            print("correspondance : ", same_points_localisation, " / total pts: ", length1 * length2)


            if same_points_localisation >= (int(length1 * length2) / 2) - 2 and length1 * length2 > 0:
                to_remove.append(i + 1)
                [cv2.circle(copy_delete, j, 2, (0, 0, 0), 2) for j in sorted_fingers[i + 1]]
                print("finger removed")

            cv2.imshow("copy_delete", copy_delete)
            cv2.waitKey(0)
            print("")


    sorted_fingers, fingers_orientation =\
                    to_removing_finger(to_remove, sorted_fingers, fingers_orientation)

    return sorted_fingers, fingers_orientation
