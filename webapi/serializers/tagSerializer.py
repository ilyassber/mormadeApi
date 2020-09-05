from rest_framework import serializers
from .. models.tag import tag

class tagSerializer(serializers.ModelSerializer):

    class Meta:
        model = tag
        fields = '__all__'