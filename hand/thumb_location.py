"""Here we recuperate skeletton points. We need to identify the position of the
thumb. By this we can search, organise and identify the finger's and their positions.
For that we compare fingertip coordiantes."""

import cv2
from scipy.spatial import distance as dist


def thumb_localisation(end_fingers, thumb):
    """Compare Thumb, fingers x and y position and determinate thumb position
    in function of them."""

    thumbx, thumby = thumb[-1][0], thumb[-1][1]                         #Thumb (x, y)
    dico_direction = {"left" :0, "right" :0, "top" :0, "bot" :0}

    for fing in end_fingers:
        fingx, fingy = fing[0], fing[1]                                 #Finger (x, y)

                                                                        #Compare Thumb - fingers
        if thumbx < fingx:      dico_direction["left"]  += 1            #x axis
        elif thumbx > fingx:    dico_direction["right"] += 1
        if thumby < fingy:      dico_direction["top"]   += 1            #y axis
        elif thumby > fingy:    dico_direction["bot"]   += 1


    if dico_direction["left"] > dico_direction["right"]:    hand = "pouce gauche"
    elif dico_direction["right"] > dico_direction["left"]:  hand = "pouce droite"

    return hand


def printing(fingers):
    """Printing for printing informations"""
    print("THUMB LOCATION")    
    print(fingers, "\n")


def thumb_location(fingers, crop):
    """Here we need - to make a treatment of the finger's, (delete false detections)
                    - recuperate end of the fingers,
                    - verify if the thumb isn't empty,
                    - localise thumb in compared fingers"""

    
    copy = crop.copy()

    printing(fingers)                                                               #1 - Print data finger's

    thumb = fingers[0]
    fingers = fingers[1:]                                                           #2 - Recuperate fingers except thumb

    end_fingers = [finger[-1] for finger in fingers if finger != []]                #4 - recuperate fingertips
    [cv2.circle(copy, fingers, 2, (255, 0, 0), 2)for fingers in end_fingers]


    if len(thumb) == 0:                                                             #5 - Empty thumb
        return False

    else:
        hand = thumb_localisation(end_fingers, thumb)                               #6 - Thumb localisation compared fingers

        cv2.circle(copy, thumb[-1], 2, (0, 0, 255), 2)
        cv2.imshow("Hand", copy)
        cv2.waitKey(0)

        print(hand, "\n")

        return hand
