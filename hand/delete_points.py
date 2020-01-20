import cv2
from scipy.spatial import distance as dist
import numpy as np











def printing():
    pass

def delete_phax(sorted_fingers, copy, last, fingers_orientation):

    print("")
    print("DELETE PHAX \n")
    print(sorted_fingers)

    sorted_fingers = set_function(sorted_fingers)

    for_display = sorted_fingers[0]
    #In case thumb has 2 points possibilities.
    a, b = point_concentration(sorted_fingers[0], last, copy, fingers_orientation)

    if a != None:
        sorted_fingers[0] = a
        fingers_orientation = b

        print("thumb points changed from : ", for_display, " to", sorted_fingers[0])

    remove = []
    for nb, finger in enumerate(sorted_fingers):

        finger = finger[1:]
        #print(finger)

        for point in range(len(finger) - 1):

            distancex = finger[point][0] - finger[point + 1][0]
            distancey = finger[point][1] - finger[point + 1][1]
            #print(  abs(distancex), abs(distancey)    )

            cv2.circle(copy, finger[point], 2, (0, 255, 255), 2)
            cv2.circle(copy, finger[point + 1], 2, (0, 0, 255), 2)
            cv2.line(copy, finger[point], finger[point + 1], (0, 0, 0), 1)


            if abs(distancex) >= 13 and abs(distancey) >= 11:
                cv2.circle(copy, finger[point + 1], 2, (255, 255, 255), 2)
                remove.append(finger[point + 1])
                finger[point + 1] = finger[point]

            elif abs(distancey) >= 20:
                cv2.circle(copy, finger[point + 1], 2, (255, 255, 255), 2)
                remove.append(finger[point + 1])
                finger[point + 1] = finger[point]


            cv2.imshow("aa", copy)
            cv2.waitKey(0)

        print("")


    sorted_fingers = removing(remove, sorted_fingers)


    for finger in sorted_fingers:
        for point in finger:
            cv2.circle(copy, point, 2, (0, 255, 0), 2)

    cv2.imshow("aa", copy)





    sorted_fingers = extremum(sorted_fingers[1:], copy)

    cv2.imshow("sorted_fingerssorted_fingers", copy)
    cv2.waitKey(0)

    print("")


    return sorted_fingers, fingers_orientation








def delete_points(sorted_fingers, fingers_orientation, last, crop):

    #Delete phax
    sorted_fingers, fingers_orientation = delete_phax(sorted_fingers, crop, last, fingers_orientation)

    #Delete finger
    sorted_fingers, fingers_orientation = delete_finger(sorted_fingers, fingers_orientation, crop)

    return sorted_fingers, fingers_orientation
