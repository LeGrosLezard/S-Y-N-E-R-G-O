"""From the MVT architecture, we are situate on the view.
It's the inteface beetween template and model (data base)"""


from django.shortcuts import render

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page

from .models import video_upload
from .forms import video_upload_form

def streaming():
    pass

def uploading(request, form):

    if request.method == 'POST':

        if form.is_valid():
            name_video = request.FILES['docfile']
            form.cleaned_data['docfile'].name
            newdoc = video_upload(docfile = request.FILES['docfile'])
            newdoc.save()
            #print("file saved into :'media'")

            return JsonResponse({"response" : "ok"})





def home(request):
    """Home template, principal template.
    Is made up of an access to the site and
    sections to present the project
    (eyes, face, head, hand, langage sections)."""

    form = video_upload_form(request.POST, request.FILES)
    uploading(request, form)


    return render(request, "Home.html", {'form':form})




def essaie(request):
    """Home template, principal template.
    Is made up of an access to the site and
    sections to present the project
    (eyes, face, head, hand, langage sections)."""

    return render(request, "essaie.html")
