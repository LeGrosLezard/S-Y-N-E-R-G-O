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

    dico_data = {"label":label, "points":points, "ratio":ratio}
    name_csv = PATH_OK_CSV + "/" + name_csv
    with open(name_csv, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=LISTE_HEADER)
        writer.writerow(dico_data)


if __name__ == "__main__":
    a = verify_length_csv("1.csv")
    print(a)
