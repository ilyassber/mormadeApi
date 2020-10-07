from django.db import models

class message(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField()
    text = models.CharField(max_length=1000, default='')
    date = models.DateField(null=True)
    time = models.DateTimeField(null=True)