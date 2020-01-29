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

    return norm, which


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


    dico_angle = {"t" : liste_angle[0:4],  "i" : liste_angle[5:8],
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




#==============================
"""Transformation of data"""
#==============================

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





