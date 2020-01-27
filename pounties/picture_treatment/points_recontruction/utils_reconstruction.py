import os
import ast
import csv
import cv2
import math
import importlib
import numpy as np
import auto_write_thread
from scipy.spatial import distance as dist



#=============================
"""Here's the csv treatment"""
#=============================


PATH_FOLDER_CSV = r"C:\Users\jeanbaptiste\Desktop\pounties\data\csv"

def csv_files():
    """We count csv files"""

    global PATH_FOLDER_CSV
    liste_csv = os.listdir(PATH_FOLDER_CSV)
    number_csv = len(liste_csv)

    return number_csv

def recuperate_data_in_csv(csv_name):
    """From csv we recuperate points data"""

    path = PATH_FOLDER_CSV + "/" + str(csv_name) + ".csv"

    liste_data = []

    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i in reader:
            liste_data.append((ast.literal_eval(i["points"]),
                               ast.literal_eval(i["ratio"]),
                               ast.literal_eval(i["label"])))

    return liste_data


def to_thread(number):

    with open('auto_write_thread.py', 'w') as file:
        file.write('import os\nimport threading')
        file.write("path = " + str(PATH_FOLDER_CSV))
    importlib.reload(auto_write_thread)





#=============================
"""Here's data treatment"""
#=============================

def drawing_circle(blank_image, points, a, b, color):
    [cv2.circle(blank_image, (j[0] + a, j[1] + b) , 2, color, 2) for i in points for j in i]


def collect_distances(points, ratio):
    """Collect Euclidean distance from each point.
    Repartite to finger's"""

    distances = []
    for nb in range(len(points)):
  
        distance = dist.euclidean(points[nb][0], points[nb][1])
        distances.append(distance)

    dico = {"t" :distances[0:4], "i" : distances[5:8], "m" : distances[9:12], "an" : distances[13:16],
            "a" : distances[17:20]}

    return dico, ratio[2] * ratio[3]


def collect_points(points):
    """Collect points and make a différence for recuperate angles
        where:   x = Xi+1 - Xi
                 y = -( Yi+1 - Yi)
    """

    abscisse = []
    for nb in range(len(points)):
        ptsX = points[nb][1][0] - points[nb][0][0]
        ptsY = - (points[nb][1][1] - points[nb][0][1])

        abscisse.append((ptsX, ptsY))

    return abscisse


def points_to_angle(abscisse):
    """Here we determinate arctangeante angle of from last abscisse
    difference in a rectangle triangle ABC:
    
                 ^       -1
        - angle acb = tan   (cb / ab)
        - if Y = 0 and X > 0 -> angle = 0°
        - if Y = 0 and X < 0 -> angle = 180°
        - if if X = 0 and Y > 0 -> angle = 90°
        - if X = 0 and Y < 0 -> angle = -90°

    - if angle < 0: angle + 180
    
    """

    liste_angle = []

    for i in abscisse:

        if i[1] == 0 and i[0] != 0:
            if i[0] > 0:    liste_angle.append(0)
            elif i[0] < 0:  liste_angle.append(180)

        elif i[0] == 0 and i[1] != 0:
            if i[1] > 0:    liste_angle.append(90)
            elif i[1] < 0:  liste_angle.append(-90)

        elif i != (0, 0):

            tan = math.atan(i[1] / i[0])
            angle = math.degrees(tan)
            if angle < 0: angle += 180
            liste_angle.append(int(angle))

        elif i == (0, 0):
            liste_angle.append(0)


    dico_angle = {"t" :liste_angle[0:4], "i" : liste_angle[5:8], "m" : liste_angle[9:12], "an" : liste_angle[13:16],
                  "a" : liste_angle[17:20]}

    return dico_angle


#============================================
"""Here's the hand need to be reconstructed
so we search points to reconstruct"""
#============================================

def what_we_need_to_search(dico_passation_distance):
    """Here we need to localised what we search.
    A finger ? a phax ? nothing ?

    #[number] as [1, 2] = phax miss
    #None = we already have all fingers
    #finger = search finger miss
    """

    dico = {"t" :[], "i" : [], "m" : [], "an" : [], "a" : []}

    for k, v in dico.items():
        phax = []

        for nb, i in enumerate(dico_passation_distance[k]):
            if i == 0.0: phax.append(nb)

        if len(phax) == 3:       dico[k].append("finger")
        elif 3 > len(phax) > 0:  dico[k] += [i for i in phax]
        elif len(phax) == 0:     dico[k].append("None")


    return dico


#============================================
"""Here's functions for compare the hand to
    reconstruct and data"""
#============================================

def determine_ratio(scale1, scale2):
    """Here make a ratio for nomalise distance,
    we need to determine the highter scale

    from the two scales and apply:
        norm = highter scale / seconde scale
    """

    if scale1 > scale2: norm = scale1 / scale2
    else: norm = scale2 / scale1
    return norm


def proximum_distance(dico_passation_distance, data_distance, norm):

    dico = {"t" :[], "i" : [], "m" : [], "an" : [], "a" : []}

    for k, v in dico.items():
        liste_working = []
        for i, j in zip(dico_passation_distance[k], data_distance[k]):
            liste_working.append(abs(i - j))

        dico[k] += [i for i in liste_working]

    return dico



#============================================
"""Search points from none detection from
    our skeletton to re built"""
#============================================

def search_points(to_search_pts, value_distance, value_angle):  


    liste = []

    for nb, i in  enumerate(to_search_pts):

        if i != None:

            if i == len(value_distance):                           
                liste.append(value_distance[nb + 1])
                liste.append(value_angle[nb + 1])

            elif i not in (0, "None", "finger"):
                liste.append(value_distance[nb + 1])
                liste.append(value_distance[nb - 1])
                liste.append(value_angle[nb + 1])
                liste.append(value_angle[nb - 1])

            elif i == 0:                                    
                liste.append(value_distance[nb + 1])
                liste.append(value_angle[nb + 1])

            elif i in ("None", "finger"):
                pass

    return liste



def finger_to_search(to_search_pts, value, dico, k):

    liste = []
    fings = ["t", "i", "m", "an", "a"]
    for i in  to_search_pts:
        if i != None:

            if i == "finger" and k not in("t", "a"):
                avant_doigt = fings.index(k) - 1
                apres_doigt = fings.index(k) + 1
                liste.append(dico[fings[avant_doigt]])
                liste.append(dico[fings[apres_doigt]])

            elif i == "finger" and k in ("t"):
                apres_doigt = fings.index(k) + 1
                liste.append(dico[fings[apres_doigt]])

            elif i == "finger" and k in ("a"):
                avant_doigt = fings.index(k) - 1
                liste.append(dico[fings[avant_doigt]])

    return liste




#===================================================
"""Search points from none detection from
    our skeletton to re built, PHAX ANGLE SECTION"""
#===================================================

def melting_angle_distance(liste_distance, liste_angle, searching_points):

    distance_angle = {"t" :[], "i" : [], "m" : [], "an" : [], "a" : []}

    for dist, angle in zip(liste_distance, liste_angle):

        for (k1, v1), (k2, v2) in zip(dist.items(), angle.items()):
            angle_distance = search_points(searching_points[k1], v1, v2)
            distance_angle[k1].append(angle_distance)

    return distance_angle


def recuperate_sum_distance_angle(distance_angle):

    sum_dist_angle = {"t" :[], "i" : [], "m" : [], "an" : [], "a" : []}

    for key, value in distance_angle.items():
        for nb, val in enumerate(value):
            if val != []:
                sum_dist_angle[key].append((sum(val), nb))

    return sum_dist_angle


def recuperate_minimum_distance_dist_angle(sum_dist_angle):

    minimum_distance_angle = []

    for k, v in sum_dist_angle.items():
        if v != []:
            a = sorted(sum_dist_angle[k], key=lambda x: x[0])
            minimum_distance_angle.append((a[0], k))

    return minimum_distance_angle

def put_informations_to_dictionnary(liste):

    info = {"t" :[], "i" : [], "m" : [], "an" : [], "a" : []}

    for i in liste:
        info[i[1]] = i[0][1]

    return info



#===================================================
"""Search points from none detection from
    our skeletton to re built, FINGERS SECTION"""
#===================================================

def recuperate_fingers_interest(liste_distance, searching_points):

    fingers = {"t" :[], "i" : [], "m" : [], "an" : [], "a" : []}
    for dist in liste_distance:           
        for key, value in i.items():
            fings = finger_to_search(searching_points[key], value, dist, key)
            fingers[k].append(fings)

    return fingers



def make_sum_finger_interest(fingers):

    sum_distance_finger = {"t" :[], "i" : [], "m" : [], "an" : [], "a" : []}

    for key, value in fingers.items():
        for nb, val in enumerate(value):

            if val != []:
                liste_working = []

                for v in val:
                    liste_working.append(v)
       
                liste_working = [j for i in liste_working for j in i]
                sum_distance_finger[key].append((sum(liste_working), nb))


    return sum_distance_finger


def minimum_fingers(sum_distance_finger):

    minimum_finger = []

    for k, v in sum_distance_finger.items():
        if v != []:

            b = sorted(v, key=lambda x: x[0])
            minimum_finger.append((b[0], k))

    return minimum_finger




if __name__ == "__main__":
    liste_video = os.listdir(r"C:\Users\jeanbaptiste\Desktop\pounties\videos")
    for i in liste_video:
        print(i)
    recuperate_data_in_csv(1)
    #to_thread(5)





