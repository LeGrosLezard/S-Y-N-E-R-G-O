from django.shortcuts import render
from .forms import video_upload_form
from django.http import HttpResponseRedirect
from .models import video_upload



def upload(request):
    """Here we uploading videos.
    For that we need a form for the template,
    if we get an answer by the template, the user,
    we verify if the form is valid. We request it, cleaning it
    upload it into a media folder and redirect user to..."""

    form = video_upload_form(request.POST, request.FILES)

    if request.method == 'POST':

        if form.is_valid():
            name_video = request.FILES['docfile']
            form.cleaned_data['docfile'].name
            newdoc = video_upload(docfile = request.FILES['docfile'])
            newdoc.save()
            return HttpResponseRedirect('')

    
      
    return render(request, 'Upload.html', {'form': form})
