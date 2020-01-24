import csv
import cv2
import os



from e_read_csv.read_csv import oppening_csv
from treat_info import transform_informations_to_data      #data to information




def write_csv(name_csv, liste_header, DICO):                             
                                                                   
    with open(name_csv, 'w') as csvfile:
        print(liste_header)
        writer = csv.DictWriter(csvfile, fieldnames=liste_header)
        writer.writeheader()
        writer.writerow(DICO)


def matching_result(informations):

    liste_header, DICO = transform_informations_to_data(informations, "0")
    write_csv("current.csv", liste_header, DICO)

    oppening_csv("current.csv")



















if __name__ == "__main__":
    #1 (31, 31, 114, 98)
    #2 (21, 36, 132, 108)
    #3 (31, 15, 98, 105)
    #4 (31, 31, 114, 111)


    #a (31, 31, 113, 109)
    informations =[[(4, 'thumb'), (4, 'I'), (2, 'M'), (None, 'An'), (4, 'a')], [[31.016124838541646, 50.44799302251776, 50.44799302251776, 51.86520991955976, ('thumb', 'I')], [11.40175425099138, 15.0, None, None, ('I', 'M')], [None, None, None, None, ('M', 'An')], [None, None, None, None, ('An', 'a')]], [[75.34284600441728, 57.58709528601257, 50.39312284879298, ('thumb', 'I')], [33.55730976192071, None, None, ('I', 'M')], [None, None, None, ('M', 'An')], [None, None, None, ('An', 'a')]], [('gauche haut', ('I', 'thumb')), ('gauche bas', ('M', 'I')), ('gauche bas', ('An', 'M')), (None, (None, None))], {'thumb': [21.095023109728988, 16.55294535724685, 10.770329614269007, 48.41829808124485], 'I': [21.213203435596427, 8.0, 7.0, 36.21320343559643], 'M': [25.0, None, None, 25.0], 'An': [None, None, None, 0], 'a': [9.899494936611665, 5.0, 4.123105625617661, 19.022600562229325]}, [['droite haut', 'droite haut', 'droite haut'], ['gauche haut', 'droite haut', 'droite haut'], ['gauche haut', None, None], [None, None, None], ['gauche haut', 'gauche bas', 'droite haut']], [[18, 7, 4, 'thumb'], [3, 3, 3, 'I'], [7, None, None, 'M'], [None, None, None, 'An'], [7, 4, 1, 'a']], {'thumb': '130-150', 'I': '80-110', 'M': '60-80', 'An': None, 'a': '20-60'}]
    
    matching_result(informations)

















