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

    return {"t" : points_treat[0:4],  "i" : points_treat[5:8],
            "m" : points_treat[9:12], "an" : points_treat[13:16],
            "a" : points_treat[17:20]}


def element_to_dict(points):

    return {"t" : points[0:4],  "i" : points[5:8],
            "m" : points[9:12], "an" : points[13:16],
            "a" : points[17:20]}

def dict_to_list(points):
    liste = []
    for k, v in points.items():
        for i in v:
            try:
                liste.append(tuple(i))
            except:
                pass
    return liste

#==============================
"""REPLACING POINTS"""
#==============================

def recuperation_of_points(informations):

    distance_list, angulus_list, scale_list, scale,\
                   minimal, index, finger_name = informations

    if minimal != None:
        minimal_index_data = minimal[1]

        distance_points = element_to_dict(distance_list[minimal_index_data])
        angulus_points = element_to_dict(angulus_list[minimal_index_data])

        phax_distance = distance_points[finger_name][index]
        phax_angulus = angulus_points[finger_name][index]

        scale_data = scale_list[minimal_index_data]

        if scale_data > scale:
            phax_distance = phax_distance / (scale_data/scale)
        else:
            phax_distance = phax_distance * (scale_data/scale)

        return (phax_distance, phax_angulus)
    else:
        return None


def convert(dict_points, key, index, points_to_convert):

    phax_distance, phax_angulus = points_to_convert


    to_change = dict_points[key][index]
    #reference = dict_points[key][index + 1][0]
    reference = dict_points[key][index - 1][0]
    coordX = int(phax_distance * math.cos(phax_angulus))
    coordY = int(phax_distance * math.sin(phax_angulus))

    print(coordX)
    print(coordY)

    #x = dict_points[key][index + 1][0][0] + coordX
    #y = dict_points[key][index + 1][0][1] + coordY

    x = dict_points[key][index - 1][0][0] - coordX
    y = dict_points[key][index - 1][0][1] - coordY


    to_change = ((x, y), reference)

    dict_points[key][index] = to_change

    print(dict_points[key])

    print("")


#============================================
"""SEARCH CLOSES POINTS"""
#============================================


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

        if distance1 != None and angulus1 != None:

            formula = math.sqrt( (distance1 ** 2) + (angulus1 ** 2))
            
            knn_list.append( (formula, nb) )

    return knn_list



def minimal_distance_knn(knn_list):

    minimal_distance = sorted(knn_list, key=lambda x: x[0])
    if len(minimal_distance) > 0:
        return minimal_distance[0]
    else:
        return None






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





