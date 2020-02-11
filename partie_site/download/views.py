from django.shortcuts import render
from .forms import video_upload_form
from django.http import HttpResponseRedirect
from .models import video_upload


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

        forms_video("", "")

    return render(request, 'upload/Upload.html', {'form': form})

