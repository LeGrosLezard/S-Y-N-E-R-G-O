import cv2
from scipy.spatial import distance as dist




def printing(rectangle, thumb, fingers, direction, axis):

    print("")
    print("IDENTIFY FINGERS")

    #Ratio aspect
    print("Box de la main est de: ", rectangle)
    #Need the thumb for detect the next first finger
    print(thumb)
    #Our finger's
    print(fingers)
    #Direction for the location for the next first finger
    print(direction, axis)



def draw_line_pts(copy, text, pts1, pts2):
    """Draw line and put text"""

    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    cv2.putText(copy, text, pts2, font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.line(copy, pts1, pts2, (0, 255, 0), 1)


def removing(nb, liste):
    """Remove fingers annatotation from list"""
    for i in range(nb): liste.remove(liste[0])



def ratio_choice(direction):
    """Choose the ratio length"""

    if direction in ("droite", "gauche"):   area = "width"
    elif direction in ("bas", "haut"):      area = "height"
    return area



def thumb_to_next_finger(fingers, thumb, finger_annotation,
                         copy, rectangle_w, rectangle_h, area_for_ratio):
    """Sometimes no detection of index, so we need to identify by distance
    the next finger"""


    fingers_identify = [(thumb, "thumb")]

    #Draw thumb points
    draw_line_pts(copy, "P", thumb[0][-1], thumb[0][-1])

    #Identify distance beetween first and thumb point
    thumb_index = dist.euclidean(fingers[0], thumb[0][-1])
    print(thumb_index, (rectangle_w, rectangle_h))


    #Index
    if area_for_ratio == "width" and thumb_index < rectangle_w * 0.574 or\
       area_for_ratio == "height" and thumb_index < rectangle_w * 0.574:
        fingers_identify.append((fingers[0], finger_annotation[0]))
        draw_line_pts(copy, finger_annotation[0], thumb[0][-1], fingers[0])
        removing(1, finger_annotation)

    #Major
    elif area_for_ratio == "width" and rectangle_w * 0.775 > thumb_index > rectangle_w * 0.574 or\
         area_for_ratio == "height" and rectangle_w * 0.775 > thumb_index > rectangle_w * 0.574:
        fingers_identify.append((fingers[0], finger_annotation[1]))
        draw_line_pts(copy, finger_annotation[1], thumb[0][-1], fingers[0])
        removing(2, finger_annotation)

    #Auricular
    elif 130 > thumb_index > 105:
        draw_line_pts(copy, finger_annotation[2], thumb[0][-1], fingers[0])
        fingers_identify.append((fingers[0], finger_annotation[2]))
        removing(3, finger_annotation)

    #Annular
    elif thumb_index > 130:
        draw_line_pts(copy, finger_annotation[3], thumb[0][-1], fingers[0])
        fingers_identify.append((fingers[0], finger_annotation[3]))
        removing(4, finger_annotation)


    cv2.imshow("thumb_next_finger", copy)
    cv2.waitKey(0)
      

    return fingers_identify


def fingers_distance(distance, rectangle_w, rectangle_h,
                     area_for_ratio, finger_annotation, fingers, copy, i,
                     fingersX):


    if len(fingers) < 4:

        #One point after
        if distance < rectangle_w * 0.295 and area_for_ratio == "width" or\
           distance < rectangle_w * 0.295 and area_for_ratio == "height":
            print("Moins 35")
            fingersX.append((fingers[i + 1], finger_annotation[0]))
            draw_line_pts(copy, finger_annotation[0], fingers[i], fingers[i + 1])
            removing(1, finger_annotation)

        elif len(finger_annotation) == 1:
            print("reste plus qu'un doigt")
            draw_line_pts(copy, finger_annotation[0], fingers[i], fingers[i + 1])
            fingersX.append((fingers[i + 1], finger_annotation[0]))
            removing(1, finger_annotation)

        elif (rectangle_w * 0.295) * 2 > distance > rectangle_w * 0.295:
            print("1 doigt apres")
            draw_line_pts(copy, finger_annotation[1], fingers[i], fingers[i + 1])
            fingersX.append((fingers[i + 1], finger_annotation[1]))
            removing(2, finger_annotation)

        elif (rectangle_w * 0.295) * 3 > distance > (rectangle_w * 0.295) * 2:
            print("2 doigts apres")
            draw_line_pts(copy, finger_annotation[2], fingers[i], fingers[i + 1])
            fingersX.append((fingers[i + 1], finger_annotation[2]))
            removing(3, finger_annotation)

        elif (rectangle_w * 0.295) * 4 > distance > (rectangle_w * 0.295) * 3:
            print("3 doigts apres")
            draw_line_pts(copy, finger_annotation[3], fingers[i], fingers[i + 1])
            fingersX.append((fingers[i + 1], finger_annotation[3]))
            removing(4, finger_annotation)

        elif distance > (rectangle_w * 0.295) * 4:
            print("ici ecart supp a * 4")


    elif len(fingers) == 4:

        draw_line_pts(copy, finger_annotation[0], fingers[i], fingers[i + 1])
        fingersX.append((fingers[i + 1], finger_annotation[0]))
        removing(1, finger_annotation)





    cv2.imshow("thumb_next_finger", copy)
    cv2.waitKey(0)
    print("")



def releve_data_thumb_fingers(points, thumb):
    """We need thumb/fingers space for releve ratio"""

    reorganisation = []

    #We can have a bad sorted of fingers.
    #So we verify a last time distance by contribution of thumb.
    no_sorted_distance = [dist.euclidean(i, thumb[0][-1]) for i in points]
    sorted_distance = sorted([dist.euclidean(i, thumb[0][-1]) for i in points])

    #good.
    if no_sorted_distance == sorted_distance:

        print("ok good sort thumb - fingers")
        for pts in points:
            if pts != (): print(dist.euclidean(pts, thumb[0][-1]))


    #not good; sort finger's a last time.
    else:
        print("\n \n re organisation of data")
        reorganisation += [pts for sorted_pts in sorted_distance for pts in points
                           if pts != () and dist.euclidean(pts, thumb[0][-1]) == sorted_pts]

        points = reorganisation
        for pts in points:
            if pts != ():
                print(dist.euclidean(pts, thumb[0][-1]))

    return points
            



def appropriate_finger_points(fingers, all):

    print("")

    end = [(j, i[1]) for i in fingers[1:] for j in all if i[0] == j[0][-1]]
    end = end + [fingers[0]]

    return end


def identify_fingers(thumb, fingers, crop, rectangle, direction, axis):

    all = fingers
    printing(rectangle, thumb, fingers, direction, axis)

    copy = crop.copy()
    finger_annotation = ["I", "M", "An", "a"]

    _, _, rectangle_w, rectangle_h = rectangle

    #Add None then replace by ()
    fingers += [None for i in range(4 - len(fingers))]
    fingers = [(lambda x: () if x == None else x[0][-1])(i) for i in fingers]
    print(fingers)
    print(len(fingers) == fingers.count(()))
    print(thumb)
    print(thumb != ())
    print("ici")
    if len(fingers) > fingers.count(()):
    
        #Choice area in function of hand position
        area_for_ratio = ratio_choice(direction)


        #Reorganise a last time
        fingers = releve_data_thumb_fingers(fingers, thumb)

        #Identify finger after the thumb
        first_fingerX = thumb_to_next_finger(fingers, thumb, finger_annotation, copy,
                             rectangle_w, rectangle_h, area_for_ratio)

        fingersX = []
        for i in range(len(fingers)):
            print("\n", finger_annotation)

            if i < len(fingers) - 1 and fingers[i] != () and fingers[i + 1] != ():

                distance = dist.euclidean(fingers[i], fingers[i + 1])
                print(distance, (rectangle_w, rectangle_h))

                fingers_distance(distance, rectangle_w, rectangle_h,
                                 area_for_ratio, finger_annotation, fingers, copy, i,
                                 fingersX)


        if len(finger_annotation) > 0: print("manque des doigts :", finger_annotation)
            

    elif fingers.count(()) == len(fingers) and thumb != ():
        draw_line_pts(copy, "P", thumb[0][-1], thumb[0][-1])
        cv2.imshow("only thumb", copy)
        cv2.waitKey(0)


    else:
        print("None")



    fingers = first_fingerX + fingersX
    fingers = appropriate_finger_points(fingers, all)
    print(fingers)
    for i in fingers:
        print(i)



    return fingers









