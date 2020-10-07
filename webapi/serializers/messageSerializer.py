from rest_framework import serializers
from .. models.message import message

class messageSerializer(serializers.ModelSerializer):

    class Meta:
        model = message
        fields = '__all__'