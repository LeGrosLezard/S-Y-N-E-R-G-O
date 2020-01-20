import cv2
from scipy.spatial import distance as dist
import numpy as np





#=========================================================================== foyers


def recuperate_distance(finger, copy):

    distance_points = [dist.euclidean(finger[i], finger[i + 1])
                       for i in range(len(finger)) if i < len(finger) - 1]

    pair = [(finger[i], finger[i + 1]) for i in range(len(finger))
            if i < len(finger) - 1]

    return pair, distance_points


def analyse_distance(distance_points):
    foyers = []

    for distance in distance_points:

        if distance > 30:    foyers.append("far")
        elif distance < 30 : foyers.append("ok")
 
    print("\n", foyers)
    return foyers



def build_foyer(f1, f2, points, copy):

    copy_foyer = copy.copy()

    #foyer1_mean = tuple(int(mean()))
    foyer1 = points[:f1]
    foyer1_mean = tuple([int(np.mean([i[0] for i in foyer1])),
                   int(np.mean([i[1] for i in foyer1]))])


    #foyer2_mean = tuple(int(mean()))
    foyer2 = points[f2:]
    foyer2_mean = tuple([int(np.mean([i[0] for i in foyer2])),
                   int(np.mean([i[1] for i in foyer2]))])

    cv2.circle(copy_foyer, foyer1[0], 20, (0, 0, 255), 2)
    cv2.circle(copy_foyer, foyer2[0], 20, (0, 0, 255), 2)

    cv2.imshow("copy_foyer", copy_foyer)
    cv2.waitKey(0)

    return foyer1_mean, foyer2_mean


def associate_foyer_to_points(foyer1_mean, foyer2_mean, points, copy):

    copy_points = copy.copy()

    foyer1 = []
    foyer2 = []

    for i in points:
        distance1 = dist.euclidean(i, foyer1_mean)
        distance2 = dist.euclidean(i, foyer2_mean)

        if distance1 > distance2:   foyer2.append(i)
        elif distance2 > distance1: foyer1.append(i)

    [cv2.circle(copy_points, i, 2, (0, 0, 255), 2) for i in foyer1]
    [cv2.circle(copy_points, i, 2, (255, 0, 0), 2) for i in foyer2]
    
    cv2.imshow("copy_points", copy_points)
    cv2.waitKey(0)


    return foyer1, foyer2


def analyse_foyers(foyers, pair, copy):

    points = list(set([j for i in pair for j in i if j != (0, 0)]))
    foyer1_mean = ""

    if foyers == ["ok", "far", "ok"]:
        print("deuxieme liaison far donc foyer apres 2 eme pts")
        foyer1_mean, foyer2_mean = build_foyer(2, 2, points, copy)

    elif foyers == ["far", "ok", "ok"]:
        print("premiere liaison foyer apres 1er pts")
        foyer1_mean, foyer2_mean = build_foyer(1, 1, points, copy)

    elif foyers == ["ok", "far"]:
        print("premier liaison")
        foyer1_mean, foyer2_mean = build_foyer(1, 1, points, copy)

    if foyers != ["ok", "ok", "ok"]:
        foyer1, foyer2 = associate_foyer_to_points(foyer1_mean, foyer2_mean, points, copy)
        return foyer1, foyer2, foyer1_mean, foyer2_mean
    else:
        return None, None, None, None


def determinate_foyer(last, foyer1, foyer2, foyer1_mean, foyer2_mean, finger):

    last_thumb_position = [i[0] for i in last if i[1] == "thumb"]


    mean_f1 = np.mean([dist.euclidean(j, foyer1_mean) for i in last_thumb_position for j in i[0]])
    mean_f2 = np.mean([dist.euclidean(j, foyer2_mean) for i in last_thumb_position for j in i[0]])

    print(mean_f1, mean_f2)
    
    if mean_f1 < mean_f2:   finger = foyer1
    elif mean_f2 < mean_f1: finger = foyer2

    return finger


def re_determinate_search_finger(fingers_orientation, last, finger):


    last_thumb_position = [i[0] for i in last if i[1] == "thumb"]

    fingers_orientation[0][0] = finger
    fingers_orientation[0][1] = last_thumb_position[0][1]

    return fingers_orientation



def point_concentration(finger, last, copy, fingers_orientation):

    print("\npoint_concentration\n")
    print(finger)



    pair, distance_points = recuperate_distance(finger, copy)
    foyers = analyse_distance(distance_points)
    foyer1, foyer2, foyer1_mean, foyer2_mean = analyse_foyers(foyers, pair, copy)
    if foyer1 != None:
        finger = determinate_foyer(last, foyer1, foyer2, foyer1_mean, foyer2_mean, finger)
        fingers_orientation = re_determinate_search_finger(fingers_orientation, last,finger)
        return finger, fingers_orientation
    else:
        return None, None





#=========================================================================== delete_phax_points
def delete_from_distance(sorted_fingers, crop):

    copy = crop.copy()

    remove = []
    for nb, finger in enumerate(sorted_fingers):

        finger = finger[1:]
        lastx_sign = ""
        lasty_sign = ""
        lastx = 0
        lasty = 0
        for point in range(len(finger) - 1):

            distancex = finger[point][0] - finger[point + 1][0]
            distancey = finger[point][1] - finger[point + 1][1]
            #print(  abs(distancex), abs(distancey)    )

            cv2.circle(copy, finger[point], 2, (0, 255, 255), 2)
            cv2.circle(copy, finger[point + 1], 2, (0, 0, 255), 2)

            cv2.line(copy, finger[point], finger[point + 1], (0, 0, 0), 1)

            print(distancex, distancey)
            
            if distancex > 0 : signx = 1
            else: signx = 0
            if distancey > 0 : signy = 1
            else: signy = 0


            print("plus grand que 20x ", abs(distancex) >= 20)
            print("pas meme signe x : ", lastx_sign != signx)

            print("plus grand que 20y ",abs(distancey) >= 20)
            print("pas meme signe y : ",lasty_sign != signy)

            print("plus grand que 17x et y > 10 ", abs(distancex) >= 17 and abs(distancey) > 10)
            print("pas meme signe 25y: ", abs(distancey) >= 25)


            if abs(distancex) >= 20 and lastx_sign != signx and lasty_sign != signy or\
               abs(distancey) >= 20 and lasty_sign != signy and lasty_sign != signy or\
               abs(distancex) >= 17 and abs(distancey) > 10 or\
               abs(distancey) >= 25:

                cv2.circle(copy, finger[point + 1], 2, (255, 255, 255), 2)
                remove.append(finger[point + 1])
                finger[point + 1] = finger[point]

            else:

                lastx_sign = signx
                lasty_sign = signy
                lastx = distancex
                lasty = distancey


            cv2.imshow("aa", copy)
            cv2.waitKey(0)

        print("")

    return remove




#=========================================================================== delete_phax

def set_function(sorted_fingers):
    """Sometimes points have same position
    need to delete the doublon so we make a set list of list"""

    set_list = []
    for i in sorted_fingers:
        if i != []:
            if i not in set_list:
                set_list.append(i)
   
    return set_list



def printing(sorted_fingers):
    print("")
    print("DELETE PHAX \n")
    print("sorted fingers: ", sorted_fingers)
    print("")


def removing(remove, sorted_fingers):

    for rem in remove:
        for finger in sorted_fingers:
            for pts in finger:
                if rem == pts:
                    finger.remove(pts)

    return sorted_fingers


def extremum(finger, copy):

    to_remove = []

    for i in finger:
        if len(i) >= 2:

            first_second_points = dist.euclidean(i[0], i[1])

            if first_second_points > 40 and len(i) == 2:
                print("second point to far")
                cv2.circle(copy, i[1], 2, (0, 0, 255), 2)
                to_remove.append(i[1])

            elif first_second_points > 40 and len(i) > 2:
                print("first or second point to far")

                second_third_points = dist.euclidean(i[1], i[2])
                if second_third_points < 20:
                    print("second and third close so first to far")
                    cv2.circle(copy, i[0], 2, (0, 0, 255), 2)
                    to_remove.append(i[0])

    for i in to_remove:
        for j in finger:
            
            for nb, k in enumerate(j):
                if k == i:
                    j.remove(k)

    return finger



def delete_phax(sorted_fingers, fingers_orientation, last, crop):

    printing(sorted_fingers)
    sorted_fingers = set_function(sorted_fingers)

    #foyer
    for_display = sorted_fingers[0]
    a, b = point_concentration(sorted_fingers[0], last, crop, fingers_orientation)

    if a != None:
        sorted_fingers[0] = a
        fingers_orientation = b

        print("thumb points changed from : ", for_display, " to", sorted_fingers[0])


    remove = delete_from_distance(sorted_fingers, crop)
    sorted_fingers = removing(remove, sorted_fingers)

    sorted_fingers[1:] = extremum(sorted_fingers[1:], crop)

    return sorted_fingers, fingers_orientation

