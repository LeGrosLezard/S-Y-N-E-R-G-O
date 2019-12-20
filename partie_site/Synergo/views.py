from django.shortcuts import render
from .forms import UploadFileForm



def Garde(request):
    return render(request, "Garde.html")

def transition(request):
    return render(request, "Transition.html")

def home(request):
    return render(request, "Home.html")

def upload(request):

    if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])
                return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    
      
    return render(request, 'Upload.html', {'form': form})


