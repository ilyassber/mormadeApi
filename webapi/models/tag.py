from django.db import models
from django.contrib.postgres.fields import ArrayField

class tag(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000, default='')
    type = models.CharField(max_length=30, null=True, blank=True)
    lvl = models.IntegerField(default=-1)
    sales = models.IntegerField(default=0)
    parents = ArrayField(models.IntegerField(), null=True, blank=True)
    childs = ArrayField(models.IntegerField(), null=True, blank=True)
    pics_list = ArrayField(models.CharField(max_length=1000), null=True, blank=True)

    def __str__(self):
        return self.name