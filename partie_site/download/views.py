from django.shortcuts import render, redirect
from .forms import video_upload_form
from django.http import HttpResponseRedirect
from .models import video_upload
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page

import base64
import urllib.request
import urllib.parse
from django.http import JsonResponse
import time
#==========================
"""User upload himself his video."""


def redirection(redirection, location):
    """Redirection on a template after have download file"""

    #if redirection is True:
        #return HttpResponseRedirect(location)
    return HttpResponseRedirect(redirection)


def forms_video():
    """Verify form, recuperate file, clean it and register it
    thank to the class into media folder."""

    if form.is_valid():
        name_video = request.FILES['docfile']
        form.cleaned_data['docfile'].name
        newdoc = video_upload(docfile = request.FILES['docfile'])
        newdoc.save()
        #print("file saved into :'media'")
#==========================






#==========================
"""Auto uplaod video from webcam user."""

def transform_camera_to_blob(url_camera):


    liste = ""
    for i in url_camera:
        liste += i
    with open("video.txt", "w") as file:
        file.write(liste)


    f = open(url_camera, 'wb')
    f.write(request.body)
    f.close()




def treat_blob_to_template():
    path = r"C:\Users\jeanbaptiste\Desktop\SYNERGO_SITE\Synergo\video.txt"

    text = ""
    with open(path, "r") as file:
        for i in file:
            text += i

    return text

#==========================


        
@cache_page(60 * 15)
@csrf_protect
def upload(request):
    """Here we uploading videos.
    For that we need a form for the template,
    if we get an answer by the template, the user,
    we verify if the form is valid. We request it, cleaning it
    upload it into a media folder and redirect user to..."""

    form = video_upload_form(request.POST, request.FILES)

    if request.method == 'POST':


        print("ouiiiiiii")


        url_camera = request.POST.get('data')


        if url_camera:


            liste = ""
            for i in url_camera:
                liste += i


        
            return JsonResponse({'results': liste})


        #else:
        #    forms_video("", "")

    return render(request, 'upload/Upload.html', {'form': form})





