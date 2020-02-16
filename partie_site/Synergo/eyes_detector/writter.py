"""We aren't in live, so we can recuperate every 1000 frames ~20 sec
with that we can take the mean eyes"""

import time
import cv2

from paths import media_path, dlib_model


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
    frame_width  = int(frame_width / number_divise)
    frame_height = int(frame_height / number_divise)

    #return video, dimensions, informations videos.
    return cap, frame_width, frame_height, number_picture, frame_sec


def video_support(frame_width, frame_height, number_picture, frame_sec):

    #Create (number_picture / 1000) supports avi files.
    #Where 1000 is number of frame who's divide number of picture into the video
    file_name = int(number_picture / 1000)
    print("Number of files: ", file_name)

    #Put it into dico
    dico_file = {}
    for nb, i in enumerate(range(file_name)):
    
        name = "data/" + str(nb) + ".avi"
        #Create (number_picture / 1000) empties videos.
                                                                  #frame/sec original video
        out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc('M','J','P','G'), int(frame_sec),
                              (frame_width,frame_height))

        dico_file[name] = out

    print("files avi created successfull")
    return dico_file



def video_writter(video):

    #Info video.
    cap, frame_width, frame_height, number_picture, frame_sec = parametrages(video)
    #Create empties video.
    dico_file = video_support(frame_width, frame_height, number_picture, frame_sec)


    file_used = 0
    nb_frame = 0

    while True:

        _, frame = cap.read()

        height, width = frame.shape[:2]

        width = int(width/2)
        height = int(height/2)

        frame = cv2.resize(frame, (width, height))


        #Every 1000 frames append a new empty video.
        file = "data/" + str(file_used) + ".avi"
        dico_file[file].write(frame)

        #File used += 1.
        #frame re initialise.
        if nb_frame == 1000:
            file_used += 1
            nb_frame = -1

        nb_frame += 1


        print(nb_frame, "file in couse :", file_used)

        cv2.imshow("Frame", frame)



        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

     
    cap.release()
    cv2.destroyAllWindows()


video  = media_path.format("aa.mp4")
video_writter(video, 2)
