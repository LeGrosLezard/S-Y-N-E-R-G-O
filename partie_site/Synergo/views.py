"""From the MVT architecture, we are situate on the view.
It's the inteface beetween template and model (data base)"""


from django.shortcuts import render

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_protect

from django.http import JsonResponse

from .models import video_upload
from .forms import video_upload_form

def treat_video(request):

    eyes_detector = request.POST.get('video_name')

    if eyes_detector:

        print(eyes_detector)
        return JsonResponse({"response" : "oki"})






@csrf_protect
def home(request):
    """Home template, principal template.
    Is made up of an access to the site and
    sections to present the project
    (eyes, face, head, hand, langage sections)."""

    form = video_upload_form(request.POST, request.FILES)

    if request.method == 'POST':

        if form.is_valid():
            name_video = request.FILES['docfile']
            form.cleaned_data['docfile'].name
            newdoc = video_upload(docfile = request.FILES['docfile'])
            newdoc.save()
 
            return JsonResponse({"response" : str(name_video)})


    return render(request, "Home.html",
                  {'form':form, "response" : "coucou"})




def essaie(request):
    """Home template, principal template.
    Is made up of an access to the site and
    sections to present the project
    (eyes, face, head, hand, langage sections)."""

    return render(request, "essaie.html")
