
import csv



#====================================== Writte in to csv ===============================
""" number phax, length phax beetween fingers, angle beetween fingers, position beetween fingers,
    length fingers, sens phaxs, width phax, position of the finger"""

liste_header = ["number phaxs;",
                "length phax1 Thumb-I;", "length phax1 I-M;", "length phax1 M-An;", "length1 phax An-a;",    #Length phaxs beetween
                "length phax2 Thumb-I;", "length phax2 I-M;", "length phax2 M-An;", "length2 phax An-a;",
                "length phax3 Thumb-I;", "length phax3 I-M;", "length phax3 M-An;", "length3 phax An-a;",
                "length phax4 Thumb-I;", "length phax4 I-M;", "length phax4 M-An;", "length4 phax An-a;",

                "angle1 thumb-I;", "angle1 I-M;", "angle1 M-An;", "angle1 An-a;",                             #angle phaxs
                "angle2 thumb-I;", "angle2 I-M;", "angle2 M-An;", "angle2 An-a;",
                "angle3 thumb-I;", "angle3 I-M;", "angle3 M-An;", "angle3 An-a;",

                "position thumb-I;", "position I-M;", "position M-An;", "position An-a;",

                "length thumb;", "length I;", "length M;", "length An;", "length a;",                         #Total length
                "length phax1 thumb;", "length phax1 I;", "length phax1 M;",                                  #length phaxs
                "length phax1 An;", "length phax1 a;",#1
                "length phax2 thumb;", "length phax2 I;", "length phax2 M;",
                "length phax2 An;", "length phax2 a;",#2
                "length phax3 thumb;", "length phax3 I;", "length phax3 M;",
                "length phax3 An;", "length phax3 a;",#3
                "length phax4 thumb;", "length phax4 I;", "length phax4 M;",
                "length phax4 An;", "length phax4 a;",#4

                "sens phax1 thumb;", "sens phax1 I;", "sens phax1 M;", "sens phax1 An;", "sens phax1 a;",      #sens phax
                "sens phax2 thumb;", "sens phax2 I;", "sens phax2 M;", "sens phax2 An;", "sens phax2 a;",
                "sens phax3 thumb;", "sens phax3 I;", "sens phax3 M;", "sens phax3 An;", "sens phax3 a;",
                "sens phax4 thumb;", "sens phax4 I;", "sens phax4 M;", "sens phax4 An;", "sens phax4 a;",

                "width phax1 thumb;", "width phax1 I;", "width phax1 M;", "width phax1 An;", "width phax1 a;",  #Width phaxs
                "width phax2 thumb;", "width phax2 I;", "width phax2 M;", "width phax2 An;", "width phax2 a;",
                "width phax3 thumb;", "width phax3 I;", "width phax3 M;", "width phax3 An;", "width phax3 a;",
                "width phax4 thumb;", "width phax4 I;", "width phax4 M;", "width phax4 An;", "width phax4 a;",

                "position thumb;", "position I;", "position M;", "position An;", "position a;"]





def header_csv(name_csv):                                           #Write header
                                                                    #New csv
    global liste_header

    with open(name_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=liste_header)
        writer.writeheader()

header_csv("yoyo.csv")


def transform_informations_to_data(liste):
    pass


def writting_data(name_csv, data):                                  #Add into csv

    with open(name_csv, 'a', newline='') as csvfile:
        for k, v in data.items():
            writer.writerow({str(k): str(v) + ";"})





#===================================== Verify length of csv =============================
import os

PATH_OK_CSV = r"C:\Users\jeanbaptiste\Desktop\dougy_petits_pecs\c_csv_files\ok_data"



def last_csv_into_folder():                                         #Recuperate last csv
    global PATH_OK_CSV

    liste_csv = sorted([int(i[:-4]) for i in os.listdir(PATH_OK_CSV)])
    print(liste_csv[-1])
    return liste_csv[-1]



def verify_length_csv(name):                                        #verify_length_csv
    global PATH_OK_CSV

    path = PATH_OK_CSV + "/" + str(name) + ".csv"

    data_number = 0
    with open(path, "rb") as csvfile:
        for i in csvfile:
            data_number += 1

    if data_number == 101:
        print("CSV rempli créez en un nouveau")





if __name__ == "__main__":

    last_csv = last_csv_into_folder()
    verify_length_csv(last_csv)














