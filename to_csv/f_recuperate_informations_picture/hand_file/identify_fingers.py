import cv2
from scipy.spatial import distance as dist



#================================================================================== globals functions
REMOVING = lambda liste: liste.remove(liste[0])

def draw_line_pts(copy, text, pts1, pts2):
    """Draw line and put text"""
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    cv2.putText(copy, text, pts2, font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.line(copy, pts1, pts2, (0, 255, 0), 1)




#================================================================================== thumb_to_next_finger()
def thumb_to_next_finger(fingers, thumb, finger_annotation,
                         copy, rectangle_w, rectangle_h, area_for_ratio):
    """Sometimes no detection of index, so we need to identify by distance
    the next finger"""

    fingers_identify = [((thumb, "thumb"))]

    #Draw thumb points
    draw_line_pts(copy, "P", thumb[-1], thumb[-1])

    #Identify distance beetween first and thumb point
    thumb_index = dist.euclidean(fingers[0], thumb[-1])
    print(thumb_index, (rectangle_w, rectangle_h))


    #Index
    if area_for_ratio == "width" and thumb_index < rectangle_w * 0.574 or\
       area_for_ratio == "height" and thumb_index < rectangle_h * 0.607:
        fingers_identify.append((fingers[0], finger_annotation[0]))
        draw_line_pts(copy, finger_annotation[0], thumb[-1], fingers[0])
        [REMOVING(finger_annotation) for iteration in range(1)]

    #Major
    elif area_for_ratio == "width" and rectangle_w * 0.775 > thumb_index > rectangle_w * 0.574 or\
         area_for_ratio == "height" and rectangle_h * 0.775 > thumb_index > rectangle_h * 0.607:
        fingers_identify.append((fingers[0], finger_annotation[1]))
        draw_line_pts(copy, finger_annotation[1], thumb[-1], fingers[0])
        [REMOVING(finger_annotation) for iteration in range(2)]

    #Auricular
    elif 130 > thumb_index > 105:
        draw_line_pts(copy, finger_annotation[2], thumb[-1], fingers[0])
        fingers_identify.append((fingers[0], finger_annotation[2]))
        [REMOVING(finger_annotation) for iteration in range(3)]

    #Annular
    elif thumb_index > 130:
        draw_line_pts(copy, finger_annotation[3], thumb[-1], fingers[0])
        fingers_identify.append((fingers[0], finger_annotation[3]))
        [REMOVING(finger_annotation) for iteration in range(1)]


    cv2.imshow("thumb_next_finger", copy)
    cv2.waitKey(0)
      

    return fingers_identify




#================================================================================== fingers_distance()
def fingers_distance(distance, rectangle_w, rectangle_h, area_for_ratio,
                     finger_annotation, fingers, copy, i, fingersX):

    if len(fingers) < 4:

        #One point after
        if distance < rectangle_w * 0.295 and area_for_ratio == "width" or\
           distance < rectangle_w * 0.295 and area_for_ratio == "height":
            print("Moins 35")
            fingersX.append((fingers[i + 1], finger_annotation[0]))
            draw_line_pts(copy, finger_annotation[0], fingers[i], fingers[i + 1])
            [REMOVING(finger_annotation) for iteration in range(1)]

        elif len(finger_annotation) == 1:
            print("reste plus qu'un doigt")
            draw_line_pts(copy, finger_annotation[0], fingers[i], fingers[i + 1])
            fingersX.append((fingers[i + 1], finger_annotation[0]))
            [REMOVING(finger_annotation) for iteration in range(1)]

        elif (rectangle_w * 0.295) * 2 > distance > rectangle_w * 0.295:
            print("1 doigt apres")
            draw_line_pts(copy, finger_annotation[1], fingers[i], fingers[i + 1])
            fingersX.append((fingers[i + 1], finger_annotation[1]))
            [REMOVING(finger_annotation) for iteration in range(2)]

        elif (rectangle_w * 0.295) * 3 > distance > (rectangle_w * 0.295) * 2:
            print("2 doigts apres")
            draw_line_pts(copy, finger_annotation[2], fingers[i], fingers[i + 1])
            fingersX.append((fingers[i + 1], finger_annotation[2]))
            [REMOVING(finger_annotation) for iteration in range(3)]

        elif (rectangle_w * 0.295) * 4 > distance > (rectangle_w * 0.295) * 3:
            print("3 doigts apres")
            draw_line_pts(copy, finger_annotation[3], fingers[i], fingers[i + 1])
            fingersX.append((fingers[i + 1], finger_annotation[3]))
            [REMOVING(finger_annotation) for iteration in range(4)]

        elif distance > (rectangle_w * 0.295) * 4:
            print("ici ecart supp a * 4")


    elif len(fingers) == 4:

        draw_line_pts(copy, finger_annotation[0], fingers[i], fingers[i + 1])
        fingersX.append((fingers[i + 1], finger_annotation[0]))
        [REMOVING(finger_annotation) for iteration in range(1)]

    cv2.imshow("thumb_next_finger", copy)
    cv2.waitKey(0)
    print("")






#========================================================================= identify_fingers()

def printing(rectangle, thumb, fingers):
    print("\nIDENTIFY FINGERS \n Box de la main est de: ",
          rectangle, "\n", thumb, "\n", fingers, "\n")


def ratio_choice(rectangle_w, rectangle_h):
    """Choose the ratio length"""
    if rectangle_w > rectangle_h:        area = "width"
    elif rectangle_h > rectangle_w:      area = "height"
    return area


def distance_thumb_fingers(points, thumb):
    """We need thumb/fingers space for releve ratio
    We can have a bad sorted of fingers.
    So we verify a last time distance by contribution of thumb."""

    print("\n releve_data_thumb_fingers\n", points, thumb)

    #We sort by asc data and compare it with data give before.
    no_sorted_distance = [dist.euclidean(i, thumb[-1]) for i in points if i != ()]
    sorted_distance = sorted([dist.euclidean(i, thumb[-1]) for i in points if i!= ()])

    if no_sorted_distance == sorted_distance:   #Matching distances sorted ok.
        print("\nOK sort thumb - fingers", [print(dist.euclidean(pts, thumb[-1])) for pts in points if pts != ()])

    else:                                       #Matching distances sorted error.
        print("\n\nre-organisation of data")
        reorganisation = []
        reorganisation += [pts for sorted_pts in sorted_distance for pts in points if pts != ()
                           and dist.euclidean(pts, thumb[-1]) == sorted_pts]
        points = reorganisation
        [print(dist.euclidean(pts, thumb[-1])) for pts in points if pts != ()]

    return points


def distance_resorted_beetween_fingers(current_fingers, fingers, all_finger):

    distance_to_sort = sorted([dist.euclidean(current_fingers, i) for i in fingers])
    reorganisation = []
    reorganisation += [fing for sort in distance_to_sort for fing in fingers if fing != ()
                        and dist.euclidean(current_fingers, fing) == sort]

    if fingers != reorganisation:
        print("order changed")

    else:
        reorganisation = all_finger

    return reorganisation

            

def appropriate_finger_to_his_points(fingers, original_fingers):
    """From original fingers, recuperate all point and attribuate
    it to a finger"""

    return [(j, i[1]) for i in fingers
            for j in original_fingers if i[0] == j[-1] and j != None] + [fingers[0]]
    





def identify_fingers(thumb, fingers, crop, rectangle):

    FINGER_ANNOTATION = ["I", "M", "An", "a"]

    original_fingers = fingers
    copy = crop.copy()
    _, _, rectangle_w, rectangle_h = rectangle

    printing(rectangle, thumb, fingers)


    #Add None then replace by () my first lambda so let it
    fingers += [None for i in range(4 - len(fingers))]
    fingers = [(lambda x: () if x == None else x[-1])(i) for i in fingers]


    #We have fingers
    if len(fingers) > fingers.count(()):

        #Choice area in function of hand position
        area_for_ratio = ratio_choice(rectangle_w, rectangle_h)
        print("\nratio choosen: ", area_for_ratio)

        #Reorganise a last time
        fingers = distance_thumb_fingers(fingers, thumb)

        #Identify finger after the thumb
        first_fingerX = thumb_to_next_finger(fingers, thumb, FINGER_ANNOTATION, copy,
                             rectangle_w, rectangle_h, area_for_ratio)

        fingersX = []


        for i in range(len(fingers)):
            print("\n", FINGER_ANNOTATION)

            if i < len(fingers) - 1 and fingers[i] != () and fingers[i + 1] != ():

                print(fingers[i], fingers[i + 1])

                fingers = distance_resorted_beetween_fingers(fingers[i], fingers[i:], fingers)

                distance = dist.euclidean(fingers[i], fingers[i + 1])
                print(distance, (rectangle_w, rectangle_h))

                fingers_distance(distance, rectangle_w, rectangle_h,
                                 area_for_ratio, FINGER_ANNOTATION, fingers, copy, i,
                                 fingersX)



        fingers = first_fingerX + fingersX
        fingers = appropriate_finger_to_his_points(fingers, original_fingers)

    #Only have Thumb finger
    elif fingers.count(()) == len(fingers) and thumb != ():
        draw_line_pts(copy, "P", thumb[-1], thumb[-1])
        cv2.imshow("only thumb", copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    else:
        print("None")




    if len(FINGER_ANNOTATION) > 0: print("\nmanque des doigts :", FINGER_ANNOTATION)
    [print(i) for i in fingers]


    return fingers








