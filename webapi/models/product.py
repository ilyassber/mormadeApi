from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField

class product(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    maker_id = models.IntegerField(default=-1)
    maker_name = models.CharField(max_length=50, default='moroccan')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, default='')
    region = models.CharField(max_length=255, default='')
    price = models.IntegerField()
    rate = models.FloatField(null=True)
    sales = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=True)
    quantity = models.IntegerField(default=1)
    promotion = models.IntegerField(default=0)
    tags = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    pics_list = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    images = ArrayField(JSONField(), null=True, blank=True)

    def __str__(self):
        return self.name
