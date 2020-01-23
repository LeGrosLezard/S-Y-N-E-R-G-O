
import csv



#====================================== Writte in to csv ===============================
""" number phax, length phax beetween fingers, angle beetween fingers, position beetween fingers,
    length fingers, sens phaxs, width phax, position of the finger"""


def header_csv(name_csv, liste_header):                             #Write header
                                                                    #New csv

    with open(name_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=liste_header)
        writer.writeheader()


def writting_data(name_csv, liste_header, data):                    #Add into csv

    with open(name_csv, 'a', newline='') as csvfile:
        for k, v in data.items():
            csvfile.write(str(v) + ";")





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

def verify_header_present():
    pass

def add_label():
    pass

#===================================== Treatment information =============================
#Conception problem, yes, but u didn't see the graph !


def transform_informations_to_data(informations):

    DICO = {
            "label;": "a faire",
            "number phaxs Thumb;":informations[0][0][0], "number phaxs I;":informations[0][1][0],                       #Numbers phaxs
            "number phaxs M;":informations[0][2][0], "number phaxs An;":informations[0][3][0],
            "number phaxs A;":informations[0][4][0],
                                                                                                                        #Length phaxs beetween
            "length phax1 Thumb-I;":informations[1][0][0], "length phax2 Thumb-I;":informations[1][0][1],
            "length phax3 Thumb-I;":informations[1][0][2], "length phax4 Thumb-I;":informations[1][0][3],


            "length phax1 I-M;":informations[1][1][0], "length phax2 I-M;":informations[1][1][1],
            "length phax3 I-M;":informations[1][1][2], "length phax4 I-M;":informations[1][1][3],


            "length phax1 M-An;":informations[1][2][0], "length phax2 M-An;":informations[1][2][1],
            "length phax3 M-An;":informations[1][2][2], "length phax4 M-An;":informations[1][2][3],

            "length1 phax An-a;":informations[1][3][0], "length2 phax An-a;":informations[1][3][1],
            "length3 phax An-a;":informations[1][3][2], "length4 phax An-a;":informations[1][3][3],


                                                                                                                        #angle phaxs
            "angle1 thumb-I;":informations[2][0][0], "angle2 thumb-I;":informations[2][0][1],
            "angle3 thumb-I;":informations[2][0][2],

            "angle1 I-M;":informations[2][1][0], "angle2 I-M;":informations[2][1][1],
            "angle3 I-M;":informations[2][1][2],

            "angle1 M-An;":informations[2][2][0], "angle2 M-An;":informations[2][2][1],
            "angle3 M-An;":informations[2][2][2],

            "angle1 An-a;":informations[2][3][0], "angle2 An-a;":informations[2][3][1],
            "angle3 An-a;":informations[2][3][2],


            "position thumb-I;":informations[3][0][0], "position I-M;":informations[3][1][0],
            "position M-An;":informations[3][2][0], "position An-a;":informations[3][3][0],

            
                                                                                                                        #Total length
                                                                                                                        
            "length thumb;":informations[4]['thumb'][-1], "length I;":informations[4]['I'][-1],
            "length M;":informations[4]['M'][-1], "length An;":informations[4]['An'][-1],
            "length a;":informations[4]['a'][-1],


                                                                                                                        #length phaxs
            "length phax1 thumb;":informations[4]['thumb'][0], "length phax2 thumb;":informations[4]['thumb'][1],
            "length phax3 thumb;":informations[4]['thumb'][2],

            "length phax1 I;":informations[4]['I'][0], "length phax2 I;":informations[4]['I'][1],
            "length phax3 I;":informations[4]['I'][2],

            "length phax1 M;":informations[4]['M'][0], "length phax2 M;":informations[4]['M'][1],
            "length phax3 M;":informations[4]['M'][2],

            "length phax1 An;":informations[4]['An'][0], "length phax2 An;":informations[4]['An'][1],
            "length phax3 An;":informations[4]['An'][2],

            "length phax1 a;":informations[4]['a'][0], "length phax2 a;":informations[4]['a'][1],
            "length phax3 a;":informations[4]['a'][2],

                                                                                                                        #sens phax

            "sens phax1 thumb;":informations[5][0][0], "sens phax2 thumb;":informations[5][0][1],
            "sens phax3 thumb;":informations[5][0][2],

            
            "sens phax1 I;":informations[5][1][0], "sens phax2 I;":informations[5][1][1],
            "sens phax3 I;":informations[5][1][2],


            "sens phax1 M;":informations[5][2][0], "sens phax2 M;":informations[5][2][1],
            "sens phax3 M;":informations[5][2][2],
            
            "sens phax1 An;":informations[5][3][0], "sens phax2 An;":informations[5][3][1],
            "sens phax3 An;":informations[5][3][2],
            
            "sens phax1 a;":informations[5][4][0], "sens phax2 a;":informations[5][4][1],
            "sens phax3 a;":informations[5][4][2],


                                                                                                                        #Width phax
            "width phax1 thumb;":informations[6][0][0], "width phax2 thumb;":informations[6][0][1],
            "width phax3 thumb;":informations[6][0][2], 

            
            "width phax1 I;":informations[6][1][0], "width phax2 I;":informations[6][1][1],
            "width phax3 I;":informations[6][1][2],
            
            "width phax1 M;":informations[6][2][0], "width phax2 M;":informations[6][2][1],
            "width phax3 M;":informations[6][2][2], 

            "width phax1 An;":informations[6][3][0], "width phax2 An;":informations[6][3][1],
            "width phax3 An;":informations[6][3][2],
            
            "width phax1 a;":informations[6][4][0], "width phax2 a;":informations[6][4][1],
            "width phax3 a;":informations[6][4][2], 


            "position thumb;":informations[7]["thumb"], "position I;":informations[7]["I"],
            "position M;":informations[7]["M"], "position An;":informations[7]["An"],
            "position a;":informations[7]["a"]}


    liste_header = [k for k, v in DICO.items()]
    return liste_header, DICO



if __name__ == "__main__":

    informations =  [[(4, 'thumb'), (4, 'I'), (4, 'M'), (4, 'An'), (4, 'a')], [[30.23243291566195, 45.254833995939045, 53.53503525729669, 60.92618484691127, ('thumb', 'I')], [13.038404810405298, 21.540659228538015, 27.784887978899608, 33.28663395418648, ('I', 'M')], [14.142135623730951, 17.46424919657298, 11.704699910719626, 9.055385138137417, ('M', 'An')], [15.297058540778355, 19.313207915827967, 22.135943621178654, 24.166091947189145, ('An', 'a')]], [[81.69489047194962, 77.16041159309584, 71.16398441859779, ('thumb', 'I')], [56.95255459239646, 55.95923498061898, 55.75198404187103, ('I', 'M')], [56.02552404970833, 25.841932763167126, 16.82869211915824, ('M', 'An')], [88.31458695977737, 64.41699802260149, 53.48736790080602, ('An', 'a')]], [('gauche haut', ('I', 'thumb')), ('gauche bas', ('M', 'I')), ('gauche bas', ('An', 'M')), ('gauche bas', ('a', 'An'))], {'thumb': [13.601470508735444, 14.142135623730951, 13.601470508735444, 41.34507664120184], 'I': [15.524174696260024, 7.615773105863909, 6.708203932499369, 29.848151734623304], 'M': [19.1049731745428, 7.0710678118654755, 7.280109889280518, 33.45615087568879], 'An': [9.899494936611665, 9.899494936611665, 5.656854249492381, 25.45584412271571], 'a': [11.704699910719626, 8.06225774829855, 7.615773105863909, 27.382730764882083]}, [['droite haut', 'droite haut', 'droite haut'], ['gauche haut', 'gauche haut', 'gauche haut'], ['gauche haut', 'gauche haut', 'gauche haut'], ['gauche haut', 'gauche haut', 'gauche haut'], ['gauche haut', 'gauche haut', 'gauche haut']], [[11, 10, 8, 'thumb'], [4, 3, 3, 'I'], [13, 7, 7, 'M'], [7, 7, 4, 'An'], [11, 7, 7, 'a']], {'thumb': '130-150', 'I': '60-80', 'M': '20-60', 'An': '20-60', 'a': '20-60'}]



    liste_header, data = transform_informations_to_data(informations)

    header_csv("yoooo.csv", liste_header)
    writting_data("yoooo.csv", liste_header, data)











