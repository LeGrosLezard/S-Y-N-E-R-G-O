from reconstruction_utils import *

points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
scale = (31, 31, 113, 109)

def passation_informations(points, scale):

    #Angulus
    angulus = collect_angulus(points)

    #Distance
    distances = collect_distances(points)

    #Scale
    scale = make_scale(scale)

    return angulus, distances, scale


def data_informations():

    scale_list = []
    angulus_list = []
    distance_list = []
    
    data_csv = recuperate_data_in_csv()

    for nb, data in enumerate(data_csv):

        pts_data, scale_data = data[0], data[1]

        #Scale
        scale_data = make_scale(scale_data)
        scale_list.append(scale_data)

        #Distance
        distances_data = collect_distances(pts_data)
        distance_list.append(distances_data)

        #Angulus
        anglulus_data = collect_angulus(pts_data)
        angulus_list.append(anglulus_data)


    return distance_list, angulus_list, scale_list, data_csv






#Passation
angulus, distances, scale = passation_informations(points, scale)

#Data
distance_list, angulus_list, scale_list, data = data_informations()


angulus = element_to_dict(angulus)
distances = element_to_dict(distances)
points = element_to_dict(points)


none = ((0, 0), (0, 0))
points = delete_points(points)
for k, v in points.items():


    for nb, i in enumerate(v):
        if i == none and nb < len(v) - 1 and v[nb + 1] != none:
            print(k, v, nb)
            if nb == 0: nb = 1
            a(distance_list, angulus_list, scale_list, k, nb, angulus, distances, scale)
            b(distance_list, angulus_list, scale_list, k, nb, angulus, distances, scale)
            c(distance_list, angulus_list, scale_list, v, angulus, distances, scale, k)
            d(distance_list, angulus_list, scale_list, v, angulus, distances, scale, k)










        elif i == none and v[nb - 1] != none:
            #print(k, v, nb)
            
            points["m"][1] = ((5, 5), (5, 5))

            

































