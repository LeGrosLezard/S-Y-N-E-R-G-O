"""From the MVT architecture, we are situate on the view.
It's the inteface beetween template and model (data base)"""


from django.shortcuts import render

#
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.http import StreamingHttpResponse
#
from django.views.decorators import gzip
#
import cv2

#Root for the eyes_sections template
from .path_views_template_root import eyes_path


def get_frame():
    camera =cv2.VideoCapture(0) 
    while True:
        _, img = camera.read()
        imgencode=cv2.imencode('.jpg',img)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

    video.release()
    

@gzip.gzip_page
def dynamic_stream(request,stream_path="video"):
    try :
        return StreamingHttpResponse(get_frame(),content_type="multipart/x-mixed-replace;boundary=frame")
    except :
        return "error"


def eyes_sections(request):
    """Eyes section present our eye project in term
    of text and eyes application (camera/eyes detector)"""

    try:
        return render(request, eyes_path)
    except:
        print("nan")






