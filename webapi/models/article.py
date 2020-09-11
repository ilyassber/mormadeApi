from django.db import models
from django.contrib.postgres.fields import ArrayField

class article(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    author_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, default='')
    cover = models.IntegerField(null=True, default=None)
    text = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    tags = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)

    def __str__(self):
        return self.title