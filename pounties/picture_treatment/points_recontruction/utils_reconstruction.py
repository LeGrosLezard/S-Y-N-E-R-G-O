import os
import ast
import csv
import cv2
import math
import importlib
import numpy as np
import auto_write_thread
from scipy.spatial import distance as dist



#============================================
"""SEARCH NONE POINTS"""
#============================================

def search_none_detections(dictionnary):
    """Only work for a dict value list"""


    for key, value in dictionnary.items():

        for nb, element in enumerate(value):
            if element == [(0, 0), (0, 0)]:
                value[nb] = None

    return dictionnary


#============================================
"""RECUPERATE ANGLES"""
#============================================

def collect_angulus(points):
    
    angulus = []
    for (pts1, pts2) in points:

        x1, y1 = pts1
        x2, y2 = pts2

        if x1 > 0 and x2 > 0:
            side = y2 - y1 / x2 - x1
            angulus.append(math.degrees(math.atan(side)))
        else:
            angulus.append(None)

    return angulus


def recuperate_angulus(angulus_list, angulus):

    angulus_knn = []
    
    for angulus_data in angulus_list:

        liste_of_liste = []

        for data, angle in zip(angulus_data, angulus):

            if data == None or angle == None:
                liste_of_liste.append(None)

            else:
                liste_of_liste.append(angle - data)

        angulus_knn.append(liste_of_liste)

    return angulus_knn


#============================================
"""RECUPERATE DISTANCE"""
#============================================


def collect_distances(points):
    """Collect Euclidean distance from each point.
    Repartite to finger's"""

    distances = []

    for (pts1, pts2) in points:

        x1, y1 = pts1
        x2, y2 = pts2

        eucli = dist.euclidean((x1, y1), (x2, y2))

        if eucli == 0:
            distances.append(None)
        else:
            distances.append(eucli)


    return distances


def make_scale(ratio):
    return ratio[2] * ratio[3]


def normalise(scale_data, scale_passation, dist_data, dist_passation):


    if scale_data > scale_passation:
        dist_data = dist_data / (scale_data / scale_passation)


    elif scale_passation > scale_data:
        dist_passation = dist_passation / (scale_passation / scale_data)  

    return (dist_passation, dist_data)


def recuperate_distance(distance_list, scale_list, distances, scale_passation):

    distance_knn = []

    for distance_data in distance_list:

        liste_of_liste = []

        for dist_data, scale_data, dist_passation in zip(distance_data, scale_list, distances):

            if dist_passation == None or dist_data == None:
                liste_of_liste.append(None)

            else:
                info = normalise(scale_data, scale_passation, dist_data, dist_passation)

                dist_passation, dist_data = info
                liste_of_liste.append(dist_passation - dist_data)

        distance_knn.append(liste_of_liste)


    return distance_knn


#============================================
"""FORMAT LIST - TUPLE
   FORMAT LIST - DICTIONNARY
"""
#============================================

def tuple_to_list(points):
    return [list(i) for i in points]


def list_to_tuple(points):
    return [tuple(i) for i in points]


def list_to_dict(points):

    points_treat = [list(i) for i in points]

    return {"t" : points_treat[0:4],  "i" : points_treat[4:8],
            "m" : points_treat[8:12], "an" : points_treat[12:16],
            "a" : points_treat[16:20]}


def element_to_dict(points):

    return {"t" : points[0:4],  "i" : points[4:8],
            "m" : points[8:12], "an" : points[12:16],
            "a" : points[16:20]}

#============================================
"""SEARCH CLOSES POINTS"""
#============================================


def recuperate_data_for_knn(dictionnary, distance_knn, angulus_knn):

    for key, value in dictionnary.items():
        print(key, value)
        for index, element in enumerate(value):

            if element == None and index == 0:
                print("case one")
                case(distance_knn, angulus_knn, key, "case_one")

            elif element == None and index == len(value) - 1:
                print("case two")
                case(distance_knn, angulus_knn, key, "case_two")

            elif element == None and index not in (0, len(value) - 1):
                print("case three")
                case_three(distance_knn, angulus_knn, key, index)
   



def case(distance_knn, angulus_knn, key, case):

    knn_list = []

    for index, (distance, angulus) in enumerate(zip(distance_knn, angulus_knn)):

        distance = element_to_dict(distance)
        angulus = element_to_dict(angulus)

        if case == "case_one":
            distance = distance[key][1]
            angulus = angulus[key][1]

        elif case == "case_two":
            distance = distance[key][-2]
            angulus = angulus[key][-2]

        if distance != None and angulus != None:

            formula = math.sqrt( (distance ** 2) + (angulus ** 2) )
            knn_list.append( (formula, index) )

    return knn_list



def case_three(distance_knn, angulus_knn, key, index):

    knn_list = []

    for nb, (distance, angulus) in enumerate(zip(distance_knn, angulus_knn)):

        distance = element_to_dict(distance)
        angulus = element_to_dict(angulus)

        distance1 = distance[key][index - 1]
        angulus1 = angulus[key][index - 1]

        distance2 = distance[key][index + 1]
        angulus2 = angulus[key][index + 1]

        if distance1 != None and angulus1 != None and\
           distance2 != None and angulus2 != None:


            formula = math.sqrt( (distance1 ** 2) + (angulus1 ** 2) +\
                                 (distance2 ** 2) + (angulus2 ** 2) )
     
            knn_list.append( (formula, nb) )

    return knn_list








#==============================
"""CSV TREATMENT"""
#==============================

PATH_FOLDER_CSV = r"C:\Users\jeanbaptiste\Desktop\pounties\data\csv"
PATH = PATH_FOLDER_CSV + "/{}.csv"

def recuperate_data_in_csv():
    """From csv we recuperate points data"""

    global PATH_FOLDER_CSV


    #number csv in folder
    csv_list = os.listdir(PATH_FOLDER_CSV)
    number_csv = len(csv_list)

    data_list = []

    for file in range(1, number_csv):

        with open(PATH.format(file), newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for information in reader:
                points = ast.literal_eval(information["points"])
                ratio =  ast.literal_eval(information["ratio"])
                label =  ast.literal_eval(information["label"])

                data_list.append((points, ratio, label))


    return data_list





