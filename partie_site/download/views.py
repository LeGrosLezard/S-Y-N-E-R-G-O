from django.shortcuts import render
from .forms import video_upload_form
from django.http import HttpResponseRedirect
from .models import video_upload
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page

import base64
import urllib.request
import urllib.parse

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

def url_treatment(url):
    """Here we just want the blob name. For that we count slash
    and at the third slash increment our url treated for return it."""

    counter = 0
    url_treated = ""
    
    for i in str(url):

        if i == "/":
            counter += 1
        if counter == 3 and i != "/":
            url_treated += i

    return url_treated

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
        #CARE MAYBE YES MAYBE NOT
        #section = request.POST.get('data')
        #if section == eyes_section:

            #forms_video()
            #redirection(False, "")
            #return render(request, 'home.html', {'form': form})

        url_camera = request.POST.get('data')
        #print(url_camera)
        if url_camera:


            print(url_camera, "0000000000000000000000000000000000\n")



            liste = ""
            for i in url_camera:
                liste += i
            with open("text.txt", "w") as file:
                file.write(liste)





            
            #data = urllib.request.urlretrieve(url_camera)
            #url_treated = url_treatment(url_camera)
            #url_treated = url_treated + ".mp4"



            #f = open(str(url_camera[27:] + ".mp4"), 'wb')
            print("oki", type(url_camera))
            f = open(url_camera, 'wb')
            print("oki", type(url_camera))
            f.write(request.body)
            f.close()



        #else:
        #    forms_video("", "")

    return render(request, 'upload/Upload.html', {'form': form})





