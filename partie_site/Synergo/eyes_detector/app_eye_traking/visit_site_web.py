import cv2
import numpy as np
from ..paths import data_save, video_save_media


def recuperate_middle_vision(position_for_hull, position, POSITION_RIGHT, POSITION_LEFT):
    """Recuperate middle of the two eyes"""

    for right, left in zip(POSITION_RIGHT, POSITION_LEFT):

        #Eye lost or blinking regulation.
        if right == [] or left == []:
            position.append(None)

        else:
            #mean of (x, y) axis.
            mid = ( int( (right[0][0] + left[0][0]) / 2 ),
                    int( (right[0][1] + left[0][1]) / 2 ))

            position_for_hull.append(mid)   #for region interest.
            position.append(mid)            #recuperate blink.


def superpose_picture(zoom, zoom_number, IMG):
    """Superpose 'eyes tracker' picture"""

    #Recuperate region zommed of the eyes movements.
    height, width = zoom.shape[:2]
    zoom = cv2.resize(zoom, (width * zoom_number, height * zoom_number))

    #Resize picture in function of the zoom.
    height, width = zoom.shape[:2]
    IMG = cv2.resize(IMG, (width, height))

    #Superpose the two picture.
    superposition = cv2.addWeighted(zoom, 0.4, IMG , 0.5, 0)

    return superposition


def first_animation(position, box, IMG):
    """Draw all points without lost points."""

    x, y, w, h = box    #region convex draw.
    blanck = np.zeros((1000, 1000, 3), np.uint8)#empty picture.

    video_name = video_save_media.format("eyes_tracking1" + ".mp4")
    writting = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'X264'), int(20), (w * 4, h * 4))

    print(w, h)

    for pos in position:
        if pos != None:

            #Draw circle on the picture.
            cv2.circle(blanck, pos, 1, (0, 0, 255), 1)

            #Recuperate region zommed of the eyes movements.
            zoom = blanck[y : y + h, x : x + w]

            superposition = superpose_picture(zoom, 4, IMG)

            writting.write(superposition)
            #cv2.imshow("superposition", superposition)
            #cv2.waitKey(100)


def second_animation(position, box, IMG):
    """Draw blink, point by point"""

    x, y, w, h = box

    video_name = video_save_media.format("eyes_tracking2" + ".mp4")
    writting = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'X264'), int(20), (w * 20, h * 20))


    for nb, i in enumerate(position):

        blanck_cinematic = np.zeros((1000, 1000, 3), np.uint8)

        if i == None:
            zoom = blanck_cinematic[y : y + h, x : x + w ]
            cv2.circle(blanck_cinematic, position[nb - 1], 3, (255, 0, 0), 1)

        else:
            zoom = blanck_cinematic[y : y + h, x : x + w]
            cv2.circle(blanck_cinematic, i, 1, (0, 0, 255), 1)

        superposition = superpose_picture(zoom, 20, IMG)
        writting.write(superposition)

        #cv2.imshow("superposition", superposition)
        #cv2.waitKey(100)


"""First main function"""
def retracage(POSITION_RIGHT, POSITION_LEFT, IMG):

    position_for_hull = []  #List region of eye position.
    position = []           #List of points with blink.

    #Mean of the two coordinates.
    recuperate_middle_vision(position_for_hull, position, POSITION_RIGHT, POSITION_LEFT)
    #Hull of points. Box of the points.
    hullConvexe = cv2.convexHull(np.array([position_for_hull]))
    box = cv2.boundingRect(hullConvexe)

    first_animation(position, box, IMG)  #All points.
    second_animation(position, box, IMG) #Point by point.

    return position, box


def mean_max_min(liste_time, mean_time, position):

    min_mean        = np.zeros((1000, 1000, 3), np.uint8)   #< mean
    maxi_mean       = np.zeros((1000, 1000, 3), np.uint8)   #> mean
    max_time        = np.zeros((1000, 1000, 3), np.uint8)   #max time
    mini_time       = np.zeros((1000, 1000, 3), np.uint8)   #min time

    for nb, i in enumerate(liste_time):

        #Maximum eye pause == 0 remove it.
        if i == max(liste_time) and nb == 0:
            liste_time.remove(i)

        #Maximum eye pause.
        elif i == max(liste_time):
            cv2.circle(max_time, position[nb], 1, (0, 0, 255), 1)

        #Minimum eye pause.
        elif i == min(liste_time):
            cv2.circle(mini_time, position[nb], 1, (0, 255, 0), 1)

        #> mean.
        elif i > mean_time:
            cv2.circle(maxi_mean, position[nb], 1, (255, 0, 0), 1)

        #< mean.
        elif i < mean_time:
            cv2.circle(min_mean, position[nb], 1, (0, 255, 0), 1)

    return [min_mean, maxi_mean, max_time, mini_time]



def quartile(liste_time, from_mean_number, picture, position):
    """Recuperate from eye position percent of the time"""

    for nb, i in enumerate(sorted(liste_time)):
        if nb >= from_mean_number * len(liste_time):
            index = liste_time.index(i)
            cv2.circle(picture, position[index], 1, (0, 255, 0), 1)


def superpose_picture_timmer(box, picture_liste, IMG):

    x, y, w, h = box    #Region convex points.

    #Run all picture time tracker.
    for nb, picture in enumerate(picture_liste):

        region = picture[y:y+h, x:x+w]
        superposition = superpose_picture(region, 20, IMG)

        image = video_save_media.format(str(nb) + ".png")
        cv2.imwrite(image, superposition)
        #cv2.imshow(str(nb), superposition)
        #cv2.waitKey(0)


"""Second main function"""
def timmer_treatment(TIMMER, position, box, IMG):

    maximaxi        = np.zeros((1000, 1000, 3), np.uint8)
    minimini        = np.zeros((1000, 1000, 3), np.uint8)

    liste_time = [TIMMER[i] - TIMMER[i -1] for i in range(len(TIMMER)) if i > 0]

    mean_time = np.mean(liste_time)

    first_picture = mean_max_min(liste_time, mean_time, position)

    quartile(liste_time, 0.90, maximaxi, position)
    quartile(liste_time, 0.25, minimini, position)

    picture_liste = first_picture + [maximaxi, minimini]

    superpose_picture_timmer(box, picture_liste, IMG)








