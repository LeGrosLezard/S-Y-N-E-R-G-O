from django.db import models

class video_upload(models.Model):
    docfile = models.FileField(upload_to='video_upload')
