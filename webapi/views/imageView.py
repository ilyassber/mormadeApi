from django.shortcuts import render
from django.conf import settings
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .. models.image import image
from .. serializers.imageSerializer import imageSerializer

class imageView(APIView):

    def options(self, request):
        response = Response()
        response['Allow'] = 'GET, POST, PUT, HEAD, OPTIONS'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, HEAD, OPTIONS'
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Request-Method'] = 'GET, POST'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, X-CSRFToken, Access-Control-Request-Method, Access-Control-Request-Headers'
        return response

    def post(self, request):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        image_serializer = imageSerializer(data=request.data)
        if image_serializer.is_valid():
            #image_serializer.data.path = 'http://localhost:3000/media/images/' + image_serializer.data.name
            #print(image_serializer.data)
            img = image_serializer.save()
            img.path = settings.HOST + '/media/images/' + str(img.image).split('/')[-1]
            img.name = img.name.split('.')[0]
            img.save()
            response.status = status.HTTP_201_CREATED
            response.data = img.id
            return response
        else:
            print('error', image_serializer.errors)
            response.status = status.HTTP_400_BAD_REQUEST
            response.data = image_serializer.errors
            return response

