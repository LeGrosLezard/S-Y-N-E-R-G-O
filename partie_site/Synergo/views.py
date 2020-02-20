"""From the MVT architecture, we are situate on the view.
It's the inteface beetween template and model (data base)"""


from django.shortcuts import render

#Json response to template
from django.http import JsonResponse

#Protection
from django.views.decorators.csrf import csrf_protect

#Uploading model/form
from .models import video_upload
from .forms import video_upload_form

from .eyes_detector.video_capture_writte import video_capture_treament
from .eyes_detector.paths import media_path, dlib_model

CHARGEMENT = 0

def verify(request):
    """Here we call this function with ajax for now if we can send response,
    the respsons is a video part.
    If chargement is egal to 3 we can send video (3 videos are writte.)."""

    global CHARGEMENT

    verification = request.POST.get('verification')
    if verification:
        return JsonResponse({"verification" : CHARGEMENT})



def uploading_file(request):
    """Here is a function for uploading files.
    We call the form, verif his validity, cleanning it, save it
    and return name of video for the next AJAX"""

    #Call form.
    form = video_upload_form(request.POST, request.FILES)

    #Post from template.²
    if request.method == 'POST':

        #Verify validity of the form.
        if form.is_valid():

            #Uploading file.
            name_video = request.FILES['docfile']                       #Recuperate the file.
            form.cleaned_data['docfile'].name                           #Cleanning.
            newdoc = video_upload(docfile = request.FILES['docfile'])   #Call model.
            newdoc.save()                                               #Saving.

            return JsonResponse({"response" : str(name_video)})


def treat_video(request):

    #We recuperate a post request = video.
    video_name = request.POST.get('video_name')
    functionality = request.POST.get('functionality')

    if video_name and functionality:

        print("searching the video into media folder : ", str(video_name))

        name_video = media_path.format(str(video_name))

        #Treat file (cut video all 20 seconds).
        video_capture_treament(name_video, dlib_model)

        return JsonResponse({"save" : "save"})



@csrf_protect
def home(request):
    """Home template, principal template. Is made up of an access to the site and
    sections to present the project (eyes, face, head, hand, langage sections)."""

    form = video_upload_form(request.POST, request.FILES)
    return render(request, "Home.html", {'form':form})




def essaie(request):
    return render(request, "essaie.html")
