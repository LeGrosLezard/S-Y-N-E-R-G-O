"""We aren't in live, so we can recuperate every 500 frames ~10-15 sec
with that we can take the mean eyes positions"""

import os
import time
import cv2

from ..paths import media_path, dlib_model, path_data_video

NUMBER_OF_FRAME = 500

def parametrages(video, number_divise):

    #Initialisze video.
    cap = cv2.VideoCapture(video)

    #Recuperate numbers picture and frame/sec
    number_picture = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_sec = cap.get(cv2.CAP_PROP_FPS)

    print("number of frame :", number_picture)
    print("number of frame/sec :", frame_sec)

    #Recuperate dimensions of the video.
    frame_width  = int(cap.get(3))
    frame_height = int(cap.get(4))

    print("dimensions to resize : ", frame_width, frame_height)

    #Divise the frame by the number_divise.
    frame_width  = int(frame_width  / number_divise)
    frame_height = int(frame_height / number_divise)

    print("resized : ", frame_width, frame_height)

    #return video, dimensions, informations videos.
    return cap, frame_width, frame_height, number_picture, frame_sec


def video_support(frame_width, frame_height, number_picture, frame_sec):

    global NUMBER_OF_FRAME

    #Create (number_picture / 500) supports avi files.
    #Where 500 is number of frame who's divide number of picture into the video
    #If video contains less 500 create one video.
    print("\nvideo contains : ", number_picture)
    if number_picture < 500:
        file_name = 1
    else:
        file_name = int(number_picture / NUMBER_OF_FRAME)

    print("Number of files: ", file_name)

    #Put it into dico
    dico_file = {}
    for nb, i in enumerate(range(file_name)):

        name = path_data_video.format(str(nb) + ".avi")

        #Create (number_picture / 500) empties videos.
                                                                  #frame/sec original video
        out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc('M','J','P','G'), int(frame_sec),
                              (frame_width, frame_height))

        dico_file[name] = out

    print("files avi created successfull")
    return dico_file


CHARGEMENT = 0
def video_writter(video, number_divise):

    global NUMBER_OF_FRAME

    #Info video.
    cap, frame_width, frame_height, number_picture, frame_sec = parametrages(video, number_divise)
    #Create empties video.
    dico_file = video_support(frame_width, frame_height, number_picture, frame_sec)


    file_used = 0
    nb_frame = 0
    start_time_appending = time.time()

    oContinuer = True
    while oContinuer:
        ret, frame = cap.read()
        if ret:
            height, width = frame.shape[:2]

            width  = int(width / number_divise)
            height = int(height / number_divise)

            frame = cv2.resize(frame, (width, height))

            #Every 500 frames append a new empty video.
            file = path_data_video.format(str(file_used) + ".avi")
            dico_file[file].write(frame)

            #File used += 1.
            #frame re initialise.
            if nb_frame == NUMBER_OF_FRAME:
                file_used += 1
                nb_frame = -1
                print("File in couse :", file_used)
                print("Took : ", time.time() - start_time_appending)

                start_time_appending = time.time()

            nb_frame += 1

            #cv2.imshow("Frame", frame)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
                #break
        else:
            oContinuer = False
    #cap.release()
    #cv2.destroyAllWindows()



def run_data_wrote():

    #Search video written from last operation and put it into a list.
    start_time_data_list = time.time()
    data = os.listdir(path_data)
    data = sorted(data)
    number_file = len(data)

    print("Count file to treat : ", number_file)
    print("running data took : ", time.time() - start_time_data_list)

    return data
