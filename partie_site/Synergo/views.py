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


def uploading_file(request):
    """Here is a function for uploading files.
    We call the form, verif his validity, cleanning it, save it
    and return name of video for the next AJAX"""

    #Call form.
    form = video_upload_form(request.POST, request.FILES)

    #Post from template.
    if request.method == 'POST':

        #Verify validity of the form.
        if form.is_valid():

            name_video = request.FILES['docfile']                       #Recuperate the file.
            form.cleaned_data['docfile'].name                           #Cleanning.
            newdoc = video_upload(docfile = request.FILES['docfile'])   #Call model.
            newdoc.save()                                               #Saving.

            return JsonResponse({"response" : str(name_video)})         #Response.




def treat_video(request):

    eyes_detector = request.POST.get('video_name')

    if eyes_detector:

        print(eyes_detector)
        return JsonResponse({"response" : "oki"})




@csrf_protect
def home(request):
    """Home template, principal template. Is made up of an access to the site and
    sections to present the project (eyes, face, head, hand, langage sections)."""

    form = video_upload_form(request.POST, request.FILES)



    return render(request, "Home.html", {'form':form})




def essaie(request):
    return render(request, "essaie.html")
