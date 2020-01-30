import os
import ast
import csv
import cv2
import math
import importlib
import numpy as np
import auto_write_thread
from scipy.spatial import distance as dist


#==============================
"""CSV TREATMENT"""
#==============================

PATH_FOLDER_CSV = r"C:\Users\jeanbaptiste\Desktop\pounties\data\csv"


def number_csv_file():

    global PATH_FOLDER_CSV
    csv_list = os.listdir(PATH_FOLDER_CSV)
    number_csv = len(csv_list)

    return number_csv


def recuperate_data_in_csv(csv_name):
    """From csv we recuperate points data"""

    global PATH_FOLDER_CSV

    path = PATH_FOLDER_CSV + "/" + str(csv_name) + ".csv"

    data_list = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for information in reader:
            points = ast.literal_eval(information["points"])
            ratio =  ast.literal_eval(information["ratio"])
            label =  ast.literal_eval(information["label"])

            data_list.append((points, ratio, label))

    return data_list



#==============================
"""NORMALIZE DISTANCES"""
#==============================

def make_ratio(ratio):
    """width picture* hight picture"""
    return ratio[2] * ratio[3]

def normalisation(ratio1, ratio2):
    """Make the ratio.
    Define the highter picture -> choice '/' or '*'."""

    if ratio1 > ratio2:
        norm = ratio1 / ratio2
        which = 1

    elif ratio2 > ratio1:
        norm = ratio2 / ratio1
        which = 2

    return (norm, which)


def collect_distances(points, which, norm, mode):
    """Collect Euclidean distance from each point.
    Repartite to finger's"""

    distances = []
    for nb in range(len(points)):

        distance = dist.euclidean(points[nb][0], points[nb][1])

        if mode is "data":
            #The data picture highter
            if which == 1:      distance = distance / norm
            #The data picture smaller
            elif which == 2:    distance = distance * norm
        distances.append(distance)

    dico = {"t" : distances[0:4],  "i" : distances[5:8],
            "m" : distances[9:12], "an" : distances[13:16],
            "a" : distances[17:20]}

    return dico





#============================================
"""RECUPERATE ANGLES"""
#============================================

def collect_coordinate(points):
    """Collect points and make a différence for recuperate angles
        where:   x = Xi+1 - Xi
                 y = - ( Yi+1 - Yi)
    """

    abscisse = []
    for nb in range(len(points)):
        ptsX = points[nb][1][0] - points[nb][0][0]
        ptsY = - (points[nb][1][1] - points[nb][0][1])
        abscisse.append((ptsX, ptsY))

    return abscisse


def points_to_angle(coordinates):
    """Here we determinate arctangeante angle of from last abscisse
        difference in a rectangle triangle ABC:
        angle acb = atan   (cb / ab)"""

    angulus_list = []

    for points in coordinates:
        x, y = points[0], points[1]

        if y == 0 and x != 0:
            if x > 0:    angulus_list.append(0)
            elif x < 0:  angulus_list.append(180)

        elif x == 0 and y != 0:
            if y > 0:    angulus_list.append(90)
            elif y < 0:  angulus_list.append(-90)

        elif points != (0, 0):
            angle = math.degrees(math.atan(y / x))
            if angle < 0: angle += 180
            angulus_list.append(int(angle))

        elif points == (0, 0):
            angulus_list.append(0)

    dico_angle = {"t" : angulus_list[0:4],  "i"  : angulus_list[5:8],
                  "m" : angulus_list[9:12], "an" : angulus_list[13:16],
                  "a" : angulus_list[17:20]}

    return dico_angle




#============================================
"""TO RECONSTRUCT"""
#============================================

def what_we_need_to_search(dico_passation_distance):
    """ phax miss = [1, 2], finger = search finger miss,
        None = ok."""

    dico = {"t" :[], "i" : [], "m" : [], "an" : [], "a" : []}

    for k, v in dico.items():
        phax = []
        for nb, i in enumerate(dico_passation_distance[k]):
            if i == 0.0: phax.append(nb)

        if len(phax) == 3:       dico[k].append("finger")
        elif 3 > len(phax) > 0:  dico[k] += [i for i in phax]
        elif len(phax) == 0:     dico[k].append("None")

    return dico


def so_we_search(none_points, points):

    search_points = []
    to_not_search = (["finger"], ["None"])

    for finger, searching in none_points.items():
        if searching not in to_not_search:

            for phax in range(len(searching)):

                #First phax
                if searching[phax] == 0 and len(searching) == 1:
                    search_points.append((finger, 1, 0))

                #[0, 1]
                elif searching[phax] == 0 and\
                     searching[phax + 1] == searching[phax] + 1:
                    print("probleme")

                #Other
                else:
                    point = searching[phax]
                    search_points.append((finger, point - 1, point))

    return search_points


def replace_point(informations, sign):

    #informations :
    #current points, name finger, phax, distance, angle, position (x, y)


    current = informations[0][informations[1]][informations[2]][0]

    if sign == "minus":
        x = current[0] - int(informations[3] * math.cos(informations[4]))
        y = current[1] - int(informations[3] * math.sin(informations[4]))
    elif sign == "add":
        x = current[0] + int(informations[3] * math.cos(informations[4]))
        y = current[1] + int(informations[3] * math.sin(informations[4]))

    informations[0][informations[1]][informations[2]][informations[5]] = (x, y)




#========================================
"""COMPAREASON OF DISTANCES"""
#========================================
def compare_distance(distance_list, distance, finger_name, phax_searching):

    compareason_list = []
    for index_data, data_dist in enumerate(distance_list):

        from_data = data_dist[finger_name][phax_searching]

        from_passation = distance[finger_name][phax_searching]

        difference = abs(from_data - from_passation)

        compareason_list.append((difference, index_data))

    return compareason_list



#========================================
"""COMPAREASON OF ANGULUS"""
#========================================

def compare_angle(angulus_list, angulus, finger_name, phax_searching):


    compareason_list = []
    for index_data, data_angulus in enumerate(angulus_list):

        from_data = data_angulus[finger_name][phax_searching]

        from_passation = angulus[finger_name][phax_searching]

        distance_difference = abs(from_data - from_passation)

        compareason_list.append((distance_difference, index_data))

    return compareason_list




#========================================
"""RECUPERATE MINIMUM VALUES"""
#========================================

def minimum_values(distance_list, anglulus_list):

    #Sorted list composed by data and index data list
    distance_list = sorted(distance_list, key=lambda x: x[0])
    anglulus_list = sorted(anglulus_list, key=lambda x: x[0])

    minimum_distance, index_distance = distance_list[0]
    minimum_angle, index_angle = anglulus_list[0]

    #Recuperate index.
    informations = (index_distance, index_angle)

    return informations


def recuperate_angle_distance(info1, info2):

    #info1 = data liste distance
    #info2 = data liste angulus

    distance = info1[0][info1[1]][info1[2]][info1[3]]
    angle = info2[0][info2[1]][info2[2]][info2[3]]

    informations = (distance, angle)

    return informations


#========================================
"""TRANSFORMATION DATA TO DICTIONNARY"""
#========================================

def points_to_fingers_dict(points):
    """
        1) - ( (0, 0), (0, 0) ) - > [ (0, 0), (0, 0) ]
        2) - { t: points, i: points ... }
    """

    points_treat = [list(i) for i in points]

    dico = {"t" : points_treat[0:4],  "i" : points_treat[5:8],
            "m" : points_treat[9:12], "an" : points_treat[13:16],
            "a" : points_treat[17:20]}

    return dico





