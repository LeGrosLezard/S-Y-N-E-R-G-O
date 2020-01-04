import cv2
import numpy as np
from matplotlib import pyplot as plt
cap = cv2.VideoCapture("v.mp4")

from sys import exit
from scipy import ndimage as ndi
from skimage.morphology import watershed, disk
from skimage import data
from skimage.io import imread
from skimage.filters import rank
from skimage.color import rgb2gray
from skimage.util import img_as_ubyte



while True:
   
    _, frame = cap.read()
    frame = cv2.resize(frame, (300, 300))

    gray = rgb2gray(frame)
    image = img_as_ubyte(gray)
    markers = rank.gradient(image, disk(5)) < 20
    markers = ndi.label(markers)[0]
    gradient = rank.gradient(image, disk(2))

    labels = watershed(gradient, markers)


     
    fig = plt.figure()
    fig.set_size_inches(1, 1, forward=False)
    axes = plt.Axes(fig, [0., 0., 1., 1.])
    axes.set_axis_off()
    fig.add_axes(axes)


    axes.imshow(image, cmap=plt.cm.gray, interpolation="nearest")

    axes.imshow(labels, cmap=plt.cm.get_cmap("Spectral"), interpolation ="nearest",
                 alpha=50)


    plt.axis("off")



 
    fig.canvas.draw()

    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8,
            sep='')
    img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    img = cv2.resize(img, (300, 300))
    cv2.imshow("plot",img)









    if cv2.waitKey(0) & 0xFF == ord('q'):
        break


 
cap.release()
cv2.destroyAllWindows()































