from rest_framework import serializers
from .. models.article import article

class articleSerializer(serializers.ModelSerializer):

    class Meta:
        model = article
        fields = '__all__'