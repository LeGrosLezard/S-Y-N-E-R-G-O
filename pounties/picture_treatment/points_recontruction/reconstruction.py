from reconstruction_utils import *














def reconstruction(points, scale):

    angulus = collect_angulus(points)
    print(angulus)

    distances = collect_distances(points)
    print(distances)

    to_search = search_none_detections(angulus, distances)
    print(to_search)

    scale = make_ratio(scale)

    scale_list = []
    angulus_list = []
    distance_list = []
    
    data_csv = recuperate_data_in_csv()

    for nb, data in enumerate(data_csv):

        pts_data, scale_data = data[0], data[1]

        scale_data = make_scale(scale_data)
        scale_list.append(scale_data)

        dist_data = collect_distances(pts_data)
        distance_list.append(dist_data)

        angle_data = collect_angulus(pts_data)
        angulus_list.append(angle_data)



    d = distance_list
    a = angulus_list
    s = scale_data
    knn_dist_list = []


    for nb, (dist, ang, sca) in enumerate(zip(d, a, s)):

        if sca > scale:
            dist = dist / (sca / scale)

        elif scale > sca:
            distances = distances / (scale / sca)

        

        knn_dist = math.sqrt((distances - dist)**2 + (angulus - ang)**2)
        knn_dist_list.append(knn_dist)


















if __name__ == "__main__":
    points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
    ratio = (31, 31, 113, 109)


    reconstruction(points, ratio)
