from django.db import models

class user(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=256, null=True)
    is_maker = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return self.username