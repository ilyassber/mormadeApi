from django.shortcuts import render
from django.conf import settings
import json
import datetime

from django.http import HttpResponse
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .. models.message import message
from .. serializers.messageSerializer import messageSerializer

class messageView(APIView):

    def registerMessage(self, data):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        serializer = messageSerializer(data = data)
        if serializer.is_valid():
            messageInstance = serializer.save()
            messageInstance.date = datetime.date.today()
            messageInstance.time = datetime.datetime.now().time()
            messageInstance.save()
            response.data = serializer.data
            response.status = status.HTTP_201_CREATED
            return response
        else:
            response.data = serializer.errors
            response.status = status.HTTP_400_BAD_REQUEST
            return response

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
        data = request.POST.dict()
        if data["operation"] == "register":
            return self.registerMessage(QueryDict(data["data"]).dict())
        else :
            response = Response()
            response['Access-Control-Allow-Origin'] = settings.HOST
            response['Access-Control-Allow-Credentials'] = 'true'
            response.data = "Baaad idea !O_o!"
            response.status = status.HTTP_400_BAD_REQUEST
            return response
