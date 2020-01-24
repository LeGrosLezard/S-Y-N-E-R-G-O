import csv
import cv2

from treat_info import transform_informations_to_data      #data to information





def matching_result(informations):

    transform_informations_to_data(informations, "_")

if __name__ == "__main__":
    #1 (31, 31, 114, 98)
    #2 (21, 36, 132, 108)
    #3 (31, 15, 98, 105)
    #4 (31, 31, 114, 111)


    #a (31, 31, 113, 109)
    informations = [[(4, 'thumb'), (4, 'I'), (2, 'M'), (0, 'An'), (4, 'a')], [[31.016124838541646, 50.44799302251776, 50.44799302251776, 51.86520991955976, ('thumb', 'I')], [11.40175425099138, 15.0, ('I', 'M')], [('M', 'An')], [('An', 'a')]], [[75.34284600441728, 57.58709528601257, 50.39312284879298, ('thumb', 'I')], [33.55730976192071, ('I', 'M')], [('M', 'An')], [('An', 'a')]], [('gauche haut', ('I', 'thumb')), ('gauche bas', ('M', 'I')), ('gauche bas', ('An', 'M'))], {'thumb': [21.095023109728988, 16.55294535724685, 10.770329614269007, 48.41829808124485], 'I': [21.213203435596427, 8.0, 7.0, 36.21320343559643], 'M': [25.0, 25.0], 'An': [0], 'a': [9.899494936611665, 5.0, 4.123105625617661, 19.022600562229325]}, [['droite haut', 'droite haut', 'droite haut'], ['gauche haut', 'droite haut', 'droite haut'], ['gauche haut'], [], ['gauche haut', 'gauche bas', 'droite haut']], [[18, 7, 4, 'thumb'], [3, 3, 3, 'I'], [7, 'M'], ['An'], [7, 4, 1, 'a']], {'thumb': '130-150', 'I': '80-110', 'M': '60-80', 'An': [], 'a': '20-60'}]

    matching_result(informations)


















