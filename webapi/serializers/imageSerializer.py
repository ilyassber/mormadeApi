from rest_framework import serializers
from .. models.image import image

class imageSerializer(serializers.ModelSerializer):

    class Meta:
        model = image
        fields = '__all__'