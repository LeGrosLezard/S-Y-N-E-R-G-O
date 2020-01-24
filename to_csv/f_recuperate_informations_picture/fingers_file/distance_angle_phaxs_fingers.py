import cv2
import math
from scipy.spatial import distance as dist


#============================================  points_distance_fingers   ==============================================

def drawing_circle(f, f1, copy):                                    #Drawing circles
    cv2.circle(copy, f1, 2, (0, 255, 0), 2)
    cv2.circle(copy, f, 2, (0, 0, 255), 2)

def drawing_line(f, f1, copy_line):                                 #Drawing lines
    cv2.line(copy_line, f1, f, (0, 0, 255), 1)

def points_distance_fingers(name, name1, dico, copy):
    """Recuperate all points distances beetween fingers
    for stock it into csv file."""

    print("fingers : ", name, name1)

    finger, finger1 = dico[name], dico[name1]                       #Recuperate points from dico

    liste_ditance = []                                              #Stock distance and names
    for f1, f in zip(finger1, finger):

        drawing_circle(f, f1, copy)

        copy_line = copy.copy()
        drawing_line(f, f1, copy_line)

        liste_ditance.append(dist.euclidean(f, f1))                 #Euclidian distances

        cv2.imshow("copy_line", copy_line)
        cv2.waitKey(0)


    for i in range(4 - len(liste_ditance)):
        liste_ditance.append(None)

    liste_ditance.append((name, name1))                             #Name's points

    return liste_ditance


#================================================  angle_points_fingers   ================================================

def drawing_triangle(f, f1, f2, copy_line):                         #Drawing triangle

    cv2.line(copy_line, f, f1, (0, 0, 255), 1)
    cv2.line(copy_line, f1, f2, (0, 0, 255), 1)
    cv2.line(copy_line, f2, f, (0, 0, 255), 1)

def draw_circle(copy, finger, finger1):                             #Drawing circle
    [cv2.circle(copy, finger[i], 2, (0, 255, 0), 2)
     for i in range(len(finger))]
    [cv2.circle(copy, finger1[i], 2, (0, 255, 0), 2)
     for i in range(len(finger1))]

def mesure_angle(pt0, pt1, pt2):                                    #Mesure angle beetween fingers
    a = int(dist.euclidean(pt1, pt2))
    b = int(dist.euclidean(pt0, pt2))
    c = int(dist.euclidean(pt0, pt1))

    a = (b**2) + (c**2) - (a**2)                                    #El Kashi
    cos = (2 * b * c)

    if cos > 0:
        angle = math.degrees(math.acos(a / cos))
        print(angle)
        return angle

def angle_points_fingers(name, name1, dico, copy):
    """Angle entre chaque doigts"""

    print("finger : ", name, name1)

    copy = copy.copy()
    finger, finger1 = dico[name], dico[name1]                       #Recuperate points from dico

    draw_circle(copy, finger, finger1)                              #Draw circles

    if len(finger) < len(finger1):      length = len(finger)        #Choice minimum length
    elif len(finger1) < len(finger):    length = len(finger1)
    else: length = len(finger)
        

    liste_angle = []
    for i in range(length):                                         #Run points
        if i <  length - 1:
            copy_triangle = copy.copy()                             #Draw triangle

            if i == 2:                                              #Last point
                try:
                    a, b, c = finger[0], finger1[i + 1], finger[i + 1]
                except IndexError:
                    try:
                        a, b, c = finger[0], finger1[i], finger[i + 1]
                    except IndexError:
                        try:
                            a, b, c = finger[0], finger1[i + 1], finger[i]
                        except IndexError:
                            pass

                angle = mesure_angle(a, b, c)
            else:                                                   #1, 2 points
                a, b, c = finger[0], finger1[i + 1], finger[i + 1]
                angle = mesure_angle(a, b, c)

            liste_angle.append(angle)                               #Add angle
            drawing_triangle(a, b, c, copy_triangle)

            cv2.imshow("copy_triangle", copy_triangle)
            cv2.waitKey(0)

    for i in range(3 - len(liste_angle)):
        liste_angle.append(None)
    liste_angle.append((name, name1))                               #Add name fingers

    return liste_angle


#=================================================  inter_espace_fingers   ==================================================
#points_distance_fingers
#angle_points_fingers

def inter_espace_fingers(dico, crop):
    """
        We recuperate angle and distance beetween each phax.
        For that we can recuperate a schema of finger's position distance openning.
    """

    distance_fingers = []
    angle_fingers = []

    liste_finger = ["thumb", "I", "M", "An", "a"]
    for i in range(len(liste_finger)):
        if i < len(liste_finger) - 1:

            distance = points_distance_fingers(liste_finger[i],                     #Distance beetween phaxs
                                               liste_finger[i + 1], dico, crop)
            distance_fingers.append(distance)

            angle = angle_points_fingers(liste_finger[i],                           #Angle beetween phaxs
                                         liste_finger[i + 1], dico, crop)
            angle_fingers.append(angle)


    print("")
    print(distance_fingers)
    print(angle_fingers)

    print("")
    
    return distance_fingers, angle_fingers



if __name__ == "__main__":

    fingers_dico = {'thumb': [(97, 105), (115, 94), (122, 79), (126, 69)], 'I': [(86, 76), (83, 55), (83, 47), (83, 40)], 'M': [(75, 79), (68, 55)], 'An': [], 'a': [(51, 98), (44, 91), (40, 94), (41, 90)]}
    image = r"C:\Users\jeanbaptiste\Desktop\dougy_petits_pecs\a_images_to_read\{}.jpg".format("a")
    img = cv2.imread(image)

    distance_fingers, angle_fingers = inter_espace_fingers(fingers_dico, img)
    print(distance_fingers, angle_fingers)

