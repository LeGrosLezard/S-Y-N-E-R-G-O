"""From the MVT architecture, we are situate on the view.
It's the inteface beetween template and model (data base)"""


from django.shortcuts import render


#Root for the eyes_sections template
from .path_views_template_root import eyes_path



def home(request):
    """Home template, principal template.
    Is made up of an access to the site and
    sections to present the project
    (eyes, face, head, hand, langage sections)."""

    return render(request, "Home.html")

def eyes_sections(request):
    """Eyes section present our eye project in term
    of text and eyes application (camera/eyes detector)"""

    return render(request, eyes_path)




def garde(request):
    #use as experience
    return render(request, "Garde.html")

def essais(request):
    #use as experience
    return render(request, "essais.html")
