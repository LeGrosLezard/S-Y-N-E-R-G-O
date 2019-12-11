import numpy as np
import matplotlib.pyplot as plt
import sys
import cv2

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
a = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\openpose\models\pose\body_25"
MODEL_FILE = a+ "\pose_deploy.prototxt"
PRETRAINED = a + "\pose_iter_584000.caffemodel"

net = cv2.dnn.readNetFromCaffe(MODEL_FILE, PRETRAINED)
print("successfully loaded classifier")


# test on a image
IMAGE_FILE = r'C:\Users\jeanbaptiste\Desktop\jgfdposgj\openpose\examples\tutorial_api_python\ici.jpg'
im = cv2.imread(IMAGE_FILE)
inpBlob = cv2.dnn.blobFromImage(im, 1.0 / 255, (im.shape[1], im.shape[0]),
                                    (0, 0, 0), swapRB=False, crop=False)


net.setInput(inpBlob)
 
output = net.forward()





points = []
 
for i in range(22):
    # confidence map of corresponding body's part.
    probMap = output[0, i, :, :]
    probMap = cv2.resize(probMap, (im.shape[1], im.shape[0]))
 
    # Find global maxima of the probMap.
    minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
 
    if prob > 0.20 :
        cv2.circle(im, (int(point[0]), int(point[1])), 8,
                   (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
        cv2.putText(im, "{}".format(i), (int(point[0]), int(point[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)
 
        # Add the point to the list if the probability is greater than the threshold
        points.append((int(point[0]), int(point[1])))
    else :
        points.append(None)
        cv2.imshow('Output-Keypoints', im)
        cv2.waitKey(0)







        
