from django.db import models

class token(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    key = models.CharField(max_length=254)
    expiration_date = models.IntegerField()
    expired = models.BooleanField(default=False)

    def __str__(self):
        return self.key