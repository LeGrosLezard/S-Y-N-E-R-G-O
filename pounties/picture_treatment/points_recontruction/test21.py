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
"""Normalize distance"""
#==============================

def make_ratio(ratio):
    w = ratio[2]
    h = ratio[3]
    return w *h

def normalisation(ratio_data, ratio_current):

    if ratio_data > ratio_current:
        norm = ratio_data / ratio_current
        which = 1

    elif ratio_current > ratio_data:
        norm = ratio_current / ratio_data
        which = 2

    return norm, which


def collect_distances(points, which, norm, mode):
    """Collect Euclidean distance from each point.
    Repartite to finger's"""


    distances = []
    for nb in range(len(points)):
  
        distance = dist.euclidean(points[nb][0], points[nb][1])

        if mode is "data":
            if which == 1:#The data picture highter
                distance = distance / norm

            elif which == 2:#The data picture smaller
                distance = distance * norm

        elif mode is "current":
            pass

        distances.append(distance)

    dico = {"t" :distances[0:4], "i" : distances[5:8], "m" : distances[9:12], "an" : distances[13:16],
            "a" : distances[17:20]}

    return dico



#============================================
"""Recuperate angles"""
#============================================

def collect_abscisse(points):
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

def points_to_angle(abscisse):
    """Here we determinate arctangeante angle of from last abscisse
    difference in a rectangle triangle ABC:

                 ^       -1
        - angle acb = tan   (cb / ab)
        - if Y = 0 and X > 0 -> angle = 0°
        - if Y = 0 and X < 0 -> angle = 180°
        - if if X = 0 and Y > 0 -> angle = 90°
        - if X = 0 and Y < 0 -> angle = -90°

    - if angle < 0: angle + 180°
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


    dico_angle = {"t" :liste_angle[0:4], "i" : liste_angle[5:8],
                  "m" : liste_angle[9:12], "an" : liste_angle[13:16],
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


def conditions_so_we_search(phax_to_search, phax, search_points, finger_name, points_current):

    if phax_to_search[phax] == 0 and len(phax_to_search) == 1:   #First phax
        search_points.append((finger_name, 1, 0))

    elif phax_to_search[phax] == 0 and\
         phax_to_search[phax + 1] == phax_to_search[phax] + 1: # [0, 1]
        print("probleme")

    else:   #Other
        search_points.append((finger_name, phax_to_search[phax] - 1, phax_to_search[phax]))



def so_we_search(miss_points, points_current):

    search_points = []
    for finger_name, phax_to_search in miss_points.items():

        if phax_to_search not in (["finger"], ["None"]): #Phax

            for phax in range(len(phax_to_search)):
                conditions_so_we_search(phax_to_search, phax, search_points, finger_name, points_current)


    return search_points

    

#=================================
"""Compare data and our points"""
#=================================

def proximum_distance(dico_passation_distance, data_distance):

    dico = {"t" :[], "i" : [], "m" : [], "an" : [], "a" : []}

    for k, v in dico.items():

        liste_working = []
        for i, j in zip(dico_passation_distance[k], data_distance[k]):
            liste_working.append(abs(i - j))

        dico[k] += [i for i in liste_working]

    return dico



#==============================
"""Transformation of data"""
#==============================

def points_to_fingers(points):

    points_treat = []
    for i in points:
        points_treat.append(list(i))

    dico = {"t" :points_treat[0:4], "i" : points_treat[5:8], "m" : points_treat[9:12],
            "an" : points_treat[13:16], "a" : points_treat[17:20]}

    return dico




#==============================
"""To clear to comment, tp forget"""
#==============================
def passation_treatment(points_current, ratio_current):


    #OUR POINTS
    ratio_current = make_ratio(ratio_current)
    distance_current = collect_distances(points_current, "", "", "current")
    #print(distance_current)

    abscisse_current = collect_abscisse(points_current)
    angle_current = points_to_angle(abscisse_current)
    #print(angle_current)


    miss_points = what_we_need_to_search(distance_current)
    points_current = points_to_fingers(points_current)
    search_points = so_we_search(miss_points, points_current)

    for k, v in points_current.items():
        print("finger ", k.upper(), v)

    print("")
    print(miss_points)
    print(search_points, "\n\n\n\n")

    return ratio_current, distance_current, angle_current, search_points, points_current



def data_treatment(csv_name, ratio_current):
    #CSV POINTS
    data_csv = recuperate_data_in_csv(csv_name)

    liste_angle = []
    liste_distance = []
    for data in data_csv:

        points_data, ratio_data = data[0], data[1]
        
        #collect normalize distances
        ratio_data = make_ratio(ratio_data)

        norm, which = normalisation(ratio_data, ratio_current)
        distance_data = collect_distances(points_data, which, norm, "data")

        #collect angles
        abscisse = collect_abscisse(points_data)
        angle_data = points_to_angle(abscisse)

        liste_angle.append(angle_data)
        liste_distance.append(distance_data)

    return liste_angle, liste_distance


def compare_distance(liste_distance, distance_current, finger_name, phax_searching):
    #DISTANCE
    liste_metablockant = []
    for index, element in enumerate(liste_distance):

        from_data = element[finger_name][phax_searching]
        from_passation = distance_current[finger_name][phax_searching]

        distance_difference = abs(from_data - from_passation)

        liste_metablockant.append((distance_difference, index))

    #print(liste_metablockant)
    return liste_metablockant



def compare_angle(liste_angle, angle_current, finger_name, phax_searching):

    #ANGLE
    liste_1 = []
    for index, element in enumerate(liste_angle):

        from_data = element[finger_name][phax_searching]
        from_passation = angle_current[finger_name][phax_searching]

        distance_difference = abs(from_data - from_passation)

        liste_1.append((distance_difference, index))

    #print(liste_1)
    return liste_1



def recuperate_minimums_values(liste_metablockant, liste_1):

    #RECUPERATE LOWER DATA
    liste_metablockant = sorted(liste_metablockant, key=lambda x: x[0])
    liste_1 = sorted(liste_1, key=lambda x: x[0])


    minimum_distance = liste_metablockant[0]
    index_minimum_distance = minimum_distance[1]

    minimum_angle = liste_1[0]
    index_minimum_angle = minimum_angle[1]

    return index_minimum_distance, index_minimum_angle


def replace_point(pts1, pts2, pts3, sign, points_current, finger_name, distance, angle):


    current = points_current[finger_name][pts1][pts2]

    if sign == "add":
        x = current[0] + int(distance * math.cos(angle))
        y = current[1] + int(distance * math.sin(angle))
    elif sign == "minus":
        x = current[0] - int(distance * math.cos(angle))
        y = current[1] - int(distance * math.sin(angle))
    points_current[finger_name][pts1][pts3] = (x, y)



def recuperate_angle_distance(liste_distance, liste_angle, index_minimum_angle,
                              index_minimum_distance, finger_name, phax_interest):

    distance = liste_distance[index_minimum_distance][finger_name][phax_interest]
    angle = liste_angle[index_minimum_angle][finger_name][phax_interest]

    return distance, angle













