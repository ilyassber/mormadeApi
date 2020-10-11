from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField

class tag(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, default='')
    type = models.CharField(max_length=50, null=True, blank=True)
    link = models.CharField(max_length=50, null=True, blank=True)
    lvl = models.IntegerField(default=-1)
    sales = models.IntegerField(default=0)
    parents = ArrayField(models.IntegerField(), null=True, blank=True)
    childs = ArrayField(models.IntegerField(), null=True, blank=True)
    pics_list = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    images = ArrayField(JSONField(), null=True, blank=True)

    def __str__(self):
        return self.name