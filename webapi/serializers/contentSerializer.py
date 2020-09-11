from rest_framework import serializers
from .. models.content import content

class contentSerializer(serializers.ModelSerializer):

    class Meta:
        model = content
        fields = '__all__'