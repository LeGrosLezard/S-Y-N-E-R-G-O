import os
import csv

PATH_OK_CSV = r"C:\Users\jeanbaptiste\Desktop\pounties\data\csv"

def verify_length_csv(name):                    #Longueur csv

    global PATH_OK_CSV

    path = PATH_OK_CSV + "/" + str(name)

    data_number = 0
    with open(path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for i in csvfile:
            data_number += 1

    if data_number >= 101:
        print("CSV rempli créez en un nouveau")
        return True

    elif data_number < 101:
        return False


def new_label(csv_name):                        #Label csv
    global PATH_OK_CSV

    csv_name = PATH_OK_CSV + "/" + csv_name
    liste = []
    with open(csv_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i in reader:
            liste.append(i["label"])

    if liste == []:
        return 1
    else:
        last_label = liste[-1]
        return int(last_label) + 1



LISTE_HEADER = ["label", "points", "ratio"]

def last_csv_into_folder():                     #Last csv name
    global PATH_OK_CSV

    liste_csv = sorted([int(i[:-4]) for i in os.listdir(PATH_OK_CSV)])

    if liste_csv == []:                                             
        liste_csv = [None]

    return liste_csv[-1]


def create_csv_header(name_csv):                #Create header

    global LISTE_HEADER
    global PATH_OK_CSV
    name_csv = PATH_OK_CSV + "/" + name_csv

    with open(name_csv, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=LISTE_HEADER)
        writer.writeheader()



def writting_data(name_csv, label, points, ratio):      #add data csv

    global LISTE_HEADER
    global PATH_OK_CSV

    dico_data = {"label":str(label), "points":points,
                 "ratio":ratio}
    name_csv = PATH_OK_CSV + "/" + name_csv
    with open(name_csv, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=LISTE_HEADER)
        writer.writerow(dico_data)


if __name__ == "__main__":


    points1 = [((88, 103), (102, 97)), ((102, 97), (113, 89)), ((113, 89), (123, 79)), ((123, 79), (131, 68)), ((88, 103), (85, 72)), ((85, 72), (81, 57)), ((81, 57), (78, 50)), ((78, 50), (75, 44)), ((88, 103), (74, 79)), ((74, 79), (61, 65)), ((61, 65), (54, 64)), ((54, 64), (47, 62)), ((88, 103), (64, 89)), ((64, 89), (57, 82)), ((57, 82), (50, 75)), ((50, 75), (46, 71)), ((88, 103), (61, 104)), ((61, 104), (50, 100)), ((50, 100), (43, 96)), ((43, 96), (36, 93))]
    ratio1 = (31, 31, 114, 98)

    create_csv_header("1.csv")

    writting_data("1.csv", 1, points1, ratio1)













