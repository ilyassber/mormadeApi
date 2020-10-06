import json
from django.conf import settings

from django.core import serializers
from django.http import HttpResponse
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .. models.tag import tag
from .. serializers.tagSerializer import tagSerializer
from .. services.api.getCookies import getCookies

class tagView(APIView):

    def getTagsByLvl(self, lvl):
        tags = tag.objects.filter(lvl=lvl)
        return tags

    def getTagsByFather(self, id):
        tags = []
        father = tag.objects.get(id=id)
        for i in father.childs:
            tags.append(tag.objects.get(id=i))
        return tags

    def options(self, request):
        response = Response()
        response['Allow'] = 'GET, POST, PUT, HEAD, OPTIONS'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, HEAD, OPTIONS'
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Request-Method'] = 'GET, POST'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, X-CSRFToken, Access-Control-Request-Method, Access-Control-Request-Headers'
        return response

    def get(self, request):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        tags = self.getTagsByLvl(0)
        serializer = tagSerializer(tags, many=True)
        response.data = serializer.data
        response.status = status.HTTP_200_OK
        return response


    def post(self, request):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        data = request.POST.dict()
        print(data)
        cookies = json.loads(str(request.COOKIES).replace("\'", "\""))
        uToken = None
        if 'utoken' in cookies:
            uToken = cookies["utoken"]
            if data['id'] != None and data['id'] != '':
                tags = tag.objects.filter(id=int(data['id']))
            elif (data['parent'] == None or data['parent'] == '') and (data['lvl'] == None or data['lvl'] == ''):
                tags = tag.objects.all()
            elif data['parent'] == None or data['parent'] == '':
                tags = self.getTagsByLvl(int(data['lvl']))
            else :
                tags = self.getTagsByFather(int(data['parent']))
            serializer = tagSerializer(tags, many=True)
            print(serializer.data)
            response.data = serializer.data
            response.status = status.HTTP_200_OK
            print(uToken)
        else:
            print("No cookies!")
            response.data = 'Error!'
            response.status = status.HTTP_200_OK
        return response