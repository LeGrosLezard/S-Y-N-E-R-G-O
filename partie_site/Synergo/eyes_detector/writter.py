import time
import cv2

from paths import media_path, dlib_model


def parametrages(video):
    
    cap = cv2.VideoCapture(video)
    number_picture = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_sec = cap.get(cv2.CAP_PROP_FPS)

    print("number of frame :", number_picture)
    print("number of frame/sec :", frame_sec)

    frame_width  = int(cap.get(3))
    frame_height = int(cap.get(4))

    print("dimensions to resize : ", frame_width, frame_height)

    frame_width  = int(frame_width/2)
    frame_height = int(frame_height/2)


    return cap, frame_width, frame_height, number_picture, frame_sec


def video_support(frame_width, frame_height, number_picture, frame_sec):


    file_name = int(number_picture / 1000)
    print("Number of files: ", file_name)

    dico_file = {}
    for nb, i in enumerate(range(file_name)):
    
        name = "data/" + str(nb) + ".avi"
        out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc('M','J','P','G'), int(frame_sec),
                              (frame_width,frame_height))

        dico_file[name] = out

    print("files avi created successfull")
    return dico_file



def video_writter(video):

    cap, frame_width, frame_height, number_picture, frame_sec = parametrages(video)
    dico_file = video_support(frame_width, frame_height, number_picture, frame_sec)


    file_used = 0
    nb_frame = 0

    while True:

        start_time_frame = time.time()

        _, frame = cap.read()

        height, width = frame.shape[:2]

        width = int(width/2)
        height = int(height/2)

        frame = cv2.resize(frame, (width, height))



        file = "data/" + str(file_used) + ".avi"
        dico_file[file].write(frame)

        if nb_frame == 1000:
            file_used += 1
            nb_frame = -1

        nb_frame += 1


        print(nb_frame, "file in couse :", file_used)

        cv2.imshow("Frame", frame)

        #print(time.time() - start_time_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

     
    cap.release()
    cv2.destroyAllWindows()


video  = media_path.format("aa.mp4")
video_writter(video)
