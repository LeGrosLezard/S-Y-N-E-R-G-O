from django import forms

class video_upload_form(forms.Form):
    title = forms.CharField(max_length=50)
    docfile = forms.FileField(label='Selectionner un fichier')
