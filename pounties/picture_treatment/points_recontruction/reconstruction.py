from reconstruction_utils import *

points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
scale = (31, 31, 113, 109)

def recuperate_points_passation(points, scale):

    angulus = collect_angulus(points)
    distances = collect_distances(points)
    scale = make_scale(scale)

    return angulus, distances, scale




def recuperate_points_data():

    scale_list = []
    angulus_list = []
    distance_list = []
    
    data_csv = recuperate_data_in_csv()

    for nb, data in enumerate(data_csv):

        pts_data, scale_data = data[0], data[1]

        scale_data = make_scale(scale_data)
        scale_list.append(scale_data)

        distances_data = collect_distances(pts_data)
        distance_list.append(distances_data)

        anglulus_data = collect_angulus(pts_data)
        angulus_list.append(anglulus_data)


    return distance_list, angulus_list, scale_list, data_csv







angulus, distances, scale = recuperate_points_passation(points, scale)
distance_list, angulus_list, scale_list, data = recuperate_points_data()



#distances = element_to_dict(distances)

kk = []
for nb, (dist_data, ang_data) in enumerate(zip(distance_list, angulus_list)):

    scale_data = scale_list[nb]

    if angulus[1] != None and distances[1] != None and\
       dist_data[1] != None and ang_data[1] != None
    if scale_data > scale:
        dist_data[1] = dist_data[1] / (scale_data/scale)
    elif scale > scale_data:
        distances[1] = distances[1] / (scale/scale_data)

    print(dist_data[1], ang_data[1], scale_data)
    print(angulus[1], distances[1], scale)


    kk.append((math.sqrt((distances[1] - dist_data[1])**2 + (angulus[1] - ang_data[1])**2), nb))

    print("")




aaaaa = sorted(kk, key=lambda x: x[0])
print(aaaaa)





























