from rest_framework import serializers
from .. models.user import user

class userSafeSerializer(serializers.ModelSerializer):

    class Meta:
        model = user
        fields = ['id', 'username', 'email']