import time
import cv2

from paths import media_path, dlib_model




video  = media_path.format("aa.mp4")


nb_frame = 0
cap = cv2.VideoCapture(video)

frame_width  = int(cap.get(3))
frame_height = int(cap.get(4))

print(frame_width, frame_height)

frame_width = int(frame_width/2)
frame_height = int(frame_height/2)
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))


while True:

    start_time_frame = time.time()

    _, frame = cap.read()

    height, width = frame.shape[:2]

    width = int(width/2)
    height = int(height/2)

    frame = cv2.resize(frame, (width, height))
    out.write(frame)

    nb_frame += 1

    cv2.imshow("Frame", frame)

    #print(time.time() - start_time_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

 
cap.release()
cv2.destroyAllWindows()
