from django.shortcuts import render





def home(request):
    return render(request, "Home.html")


def garde(request):
    return render(request, "Garde.html")

def eyes_sections(request):
    return render(request, "eyes_sections.html")

def essais(request):
    return render(request, "essais.html")
