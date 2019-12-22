from django.shortcuts import render



def essais(request):
    return render(request, "essais.html")

def Garde(request):
    return render(request, "Garde.html")

def transition(request):
    return render(request, "Transition.html")

def home(request):
    return render(request, "Home.html")




