from django.db import models
from django.contrib.postgres.fields import ArrayField

class content(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    author_id = models.IntegerField(default=-1)
    article = models.IntegerField(default=-1)
    type = models.CharField(max_length=255)
    text = models.CharField(max_length=2999, default='')
    image = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.id