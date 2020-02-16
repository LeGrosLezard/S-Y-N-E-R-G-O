import csv

LISTE_HEADER = ["label", "right_eyeX", "right_eyeY", "left_eyeX", "left_eyeY"]

def create_csv(csv_path):                #Create header

    global LISTE_HEADER

    with open(csv_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=LISTE_HEADER)
        writer.writeheader()


def writting_data(csv_path, label, points1, points2):      #add data csv

    global LISTE_HEADER

    dico_data = {"label":str(label),
                 "right_eyeX":points1[0], "right_eyeY":points1[1],
                 "left_eyeX":points2[0], "left_eyeY":points2[1]}

    with open(csv_path, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=LISTE_HEADER)
        writer.writerow(dico_data)
