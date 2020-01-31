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
"""SEARCH POINTS"""
#============================================

def search_none_detections(angulus, distances):
    search = []
    for index, (angle, distance) in enumerate(zip(angulus, distances)):
        if angle == None and distance == None:
            search.append(index)

    return search




#============================================
"""RECUPERATE ANGLES"""
#============================================

def collect_angulus(points):
    
    angulus = []
    for (pts1, pts2) in points:

        x1, y1 = pts1
        x2, y2 = pts2

        if x1 > 0 and x2 > 0:
            side = y1 - y2 / x2 - x1
            angulus.append(math.degrees(math.atan(side)))
        else:
            angulus.append(None)

    return angulus




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





#============================================
"""FORMAT LIST - TUPLE"""
#============================================

def tuple_to_list(points):
    return [list(i) for i in points]


def list_to_tuple(points):
    return [tuple(i) for i in points]





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





