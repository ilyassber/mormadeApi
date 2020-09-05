from rest_framework import serializers
from .. models.image import image

class imageDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = image
        fields = ['id', 'name', 'path']