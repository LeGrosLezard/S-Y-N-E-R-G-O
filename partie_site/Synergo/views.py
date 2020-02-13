"""From the MVT architecture, we are situate on the view.
It's the inteface beetween template and model (data base)"""


from django.shortcuts import render

def home(request):
    """Home template, principal template.
    Is made up of an access to the site and
    sections to present the project
    (eyes, face, head, hand, langage sections)."""

    return render(request, "Home.html")



def essaie(request):
    """Home template, principal template.
    Is made up of an access to the site and
    sections to present the project
    (eyes, face, head, hand, langage sections)."""

    path = r"C:\Users\jeanbaptiste\Desktop\SYNERGO_SITE\Synergo\text.txt"

    text = ""
    with open(path, "r") as file:
        for i in file:
            text += i

    return render(request, "essaie.html", {"oki" : text})
