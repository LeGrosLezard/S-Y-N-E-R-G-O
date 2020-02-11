"""From the MVT architecture, we are situate on the view.
It's the inteface beetween template and model (data base)"""


from django.shortcuts import render

def home(request):
    """Home template, principal template.
    Is made up of an access to the site and
    sections to present the project
    (eyes, face, head, hand, langage sections)."""

    return render(request, "Home.html")


def garde(request):
    #use as experience
    return render(request, "Garde.html")

def essais(request):
    #use as experience
    return render(request, "essais.html")
