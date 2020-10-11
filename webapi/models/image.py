import os
from django.db import models
from .. services.uploadToPathAndRename import UploadToPathAndRename
from django.conf import settings

class image(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=256)
    alt = models.CharField(max_length=256, default='')
    path = models.CharField(max_length=256, null=True)
    image = models.ImageField(upload_to=UploadToPathAndRename(os.path.join(settings.MEDIA_ROOT, 'images')), null=True)

    def __str__(self):
        return self.name