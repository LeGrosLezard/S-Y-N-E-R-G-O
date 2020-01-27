
"""Here's librairy treatment"""
import cv2
import ast
import math
import numpy as np
from scipy.spatial import distance as dist

"""Here's csv treatment"""
from utils_reconstruction import csv_files
from utils_reconstruction import recuperate_data_in_csv


"""Here's data treatment"""
from utils_reconstruction import collect_distances
from utils_reconstruction import *


def reconstruction(points, ratio, image):

    """Recuperate data"""
    data = recuperate_data_in_csv(1)

    """Treatement of our passation point to reconstruct"""
    #Recuperate distance, scale, angulus from points to reconstruct.
    distance, scale = collect_distances(points, ratio)

    x_y_absice = collect_points(points)
    angles = points_to_angle(x_y_absice)

    searching_points = what_we_need_to_search(distance)
    print(searching_points, "\n")


    """Begenning to compare passation and data csv"""
    liste_informations_angle = []
    liste_informations_distance = []

    for i in data:




if __name__ == "__main__":


    image = "a"
    points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
    ratio = (31, 31, 113, 109)

    reconstruction(points, ratio, image)
    













