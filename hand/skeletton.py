import cv2
import time

THRESHOLD = 0.1
INHEIGHT = 368
SCALFACTOR = 1.0/255
def find_skeleton_points(crop, protoFile, weightsFile):
    """Here we search points of hand skeletton into the picture.
    We recup points if probabily is highter to the THRESHOLD."""

    global THRESHOLD
    global SCALFACTOR

    t = time.time()

    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

    frameHeight, frameWidth = crop.shape[:2]
    aspect_ratio = frameWidth/frameHeight

    inWidth = int(((aspect_ratio*INHEIGHT)*8)//8)
    inpBlob = cv2.dnn.blobFromImage(crop, SCALFACTOR, (inWidth, INHEIGHT),
                                    (0, 0, 0), swapRB=False, crop=False)
    net.setInput(inpBlob)
    output = net.forward()

    skelettor_points = []
    for i in range(22):

        # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]
        probMap = cv2.resize(probMap, (frameWidth, frameHeight))

        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        if prob > THRESHOLD :   skelettor_points.append((int(point[0]), int(point[1])))
        else :                  skelettor_points.append(None)

    print("time taken by network : {:.3f}".format(time.time() - t))
    return skelettor_points


#=================================================================================== collect_points_skeletton()

def draw_points_skeletton(crop_copy, skelettor_points, partA, partB):
    """Draw points for have a view"""

    cv2.line(crop_copy, skelettor_points[partA], skelettor_points[partB], (0, 255, 255), 2)
    cv2.circle(crop_copy, skelettor_points[partA], 4, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
    cv2.circle(crop_copy, skelettor_points[partB], 4, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)


POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],         #Thumb
               [0,5],[5,6],[6,7],[7,8],         #Index
               [0,9],[9,10],[10,11], [11,12],   #Major
               [0,13],[13,14],[14,15],[15,16],  #Annular
               [0,17],[17,18],[18,19],[19,20] ] #Auricular


def collect_points_skeletton(crop, skelettor_points):
    """Here we recuperate pair of points.
    We define 3 lists: finger:      for have miss pair,
                       skeletton:   pair of points,
                       position :   position of pairs."""

    global POSE_PAIRS

    crop_copy = crop.copy()

    # Draw Skeleton
    finger = []
    position = []
    skeletton = []

    for nb, pair in enumerate(POSE_PAIRS):
        partA = pair[0]
        partB = pair[1]

        if skelettor_points[partA] and skelettor_points[partB]:
            draw_points_skeletton(crop_copy, skelettor_points, partA, partB)

            finger.append(nb)
            skeletton.append(pair)
            position.append((skelettor_points[partA], skelettor_points[partB]))

        else:
            position.append(((0, 0), (0, 0)))


    cv2.imshow("complete", crop_copy)
    cv2.waitKey(0)

    return skeletton, position, finger


#=================================================================================== hand_skelettor()
def hand_skelettor(crop, protoFile, weightsFile):

    #Find points
    skelettor_points = find_skeleton_points(crop, protoFile, weightsFile)
    #Collect points
    skeletton, position, finger = collect_points_skeletton(crop, skelettor_points)

    return skeletton, position, finger
