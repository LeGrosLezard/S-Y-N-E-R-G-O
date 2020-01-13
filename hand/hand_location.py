import cv2
from scipy.spatial import distance as dist

def hand_location(thumb, index, major, annular, auricular, crop):
    """Here we need to localise the thumb for have
    the hand position left or right hand.
    But hand can turn around and we hope palm area'll can
    give us that"""

    hand = ""
    copy = crop.copy()

    #We recuperate all element from pair's points; if no detection we put (0, 0)
    end_fingers = [[j for i in index for j in i if j != (0, 0)],
                   [j for i in major for j in i if j != (0, 0)],
                   [j for i in annular for j in i if j != (0, 0)],
                   [j for i in auricular for j in i if j != (0, 0)]]

    #recuperate last points of finger's (end of finger)
    end_fingers = [fingers[-1] for fingers in end_fingers if fingers != []]
    [cv2.circle(copy, fingers, 2, (255, 0, 0), 2) for fingers in end_fingers]

    #recuperate thumb last point
    thumb = [j for i in thumb for j in i if j != (0, 0)][-1]
    cv2.circle(copy, thumb, 2, (0, 0, 255), 2)

    #compare each last point finger to the thumb pts
    left = 0
    right = 0
    #if thumb to left of points left += 1 right in opposite case
    for fing in end_fingers:
        if thumb[0] < fing[0]:
            left += 1
        elif thumb[0] > fing[0]:
            right += 1

    if left > right:
        hand = "pouce gauche"
    elif right > left:
        hand = "pouce droite"
    else:
        print("probleme HAND LOCATION")

    cv2.imshow("Hand", copy)
    cv2.waitKey(0)

    print(hand)
    return hand


