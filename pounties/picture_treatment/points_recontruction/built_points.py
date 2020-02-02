from convert_variable import *


def recuperate_informations(first_part):

    data, index_distance, index_angulus,\
    distance_list, angulus_list, finger_name, value = first_part

    #Recuperate points of fingers if not (0, 0)
    none = ((0, 0), (0, 0))
    index_pair = [nb for nb, i in enumerate(value) if i == none]
    print(index_pair)

    #Ratio distance
    distance_ratio = data[index_distance][1]

    #Recuperate distance treated indexed.
    distance = distance_list[index_distance]

    #distance list to dictionnary.
    distance = element_to_dict(distance)

    #Fingers interest.
    distance = distance[finger_name]

    #Phax interest.
    distance_search = [(i, nb) for nb, i in enumerate(distance) for j in index_pair if j == nb]



    angulus = data[index_angulus][1]

    angulus = distance_list[index_angulus]
    angulus = element_to_dict(angulus)
    angulus = angulus[finger_name]
    angulus_search = [(i, nb) for nb, i in enumerate(angulus) for j in index_pair if j == nb]


    return distance_search, angulus_search, distance, angulus


def transform_to_coordinate(first_part):

    informations = recuperate_informations(first_part)
    distance_search, angulus_search, distance, angulus = informations


    print(distance_search)
    print(angulus_search)
    print(distance, angulus)


    if index == 0:
        pass


    



















