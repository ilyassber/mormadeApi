from django.shortcuts import render
from django.conf import settings
import json
from uuid import uuid4
import time;

from django.core import serializers
from django.http import HttpResponse
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .. models.user import user
from .. models.token import token
from .. serializers.userSerializer import userSerializer
from .. serializers.userSafeSerializer import userSafeSerializer
from .. services.api.getCookies import getCookies

class userView(APIView):

    def logOut(self, uToken):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        tokenInstance = token.objects.get(key=uToken)
        tokenInstance.expiration_date = 0
        tokenInstance.save()
        response['Set-Cookie'] = 'utoken=; Expires=Thu, 01 Jan 1970 00:00:01 GMT; Domain=' + settings.DOMAIN + '; Path=/; HttpOnly; SameSite=Strict'
        response.status = status.HTTP_201_CREATED
        response.data = 'logout'
        return response

    def signUp(self, data):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        is_exist = user.objects.filter(email = data["email"]).count()
        if is_exist == 0:
            hashedPassword = make_password(data["password"])
            data["password"] = hashedPassword
            serializer = userSerializer(data = data)
            response = Response()
            if serializer.is_valid():
                userInstance = serializer.save()
                rand_key = uuid4()
                tokenInstance = token.objects.create(
                    key=rand_key,
                    user_id=userInstance.id,
                    expiration_date=((3600*24*30) + time.time())
                )
                tokenInstance.save()
                print(tokenInstance.key)
                response.data = serializer.data
                print(response.data)
                response.status = status.HTTP_201_CREATED
                response['Set-Cookie'] = 'utoken=' + str(tokenInstance.key)+ "; Domain=" + settings.DOMAIN + "; Path=/; HttpOnly; SameSite=Strict"
                return response
            response.data = serializer.errors
            response.status = status.HTTP_400_BAD_REQUEST
            return response
        else:
            response.data = json.dumps({'status': 'this email is already registred!'})
            response.status = status.HTTP_208_ALREADY_REPORTED
            return response

    def login(self, data):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        userInstance = user.objects.get(email=data["email"])
        if not (userInstance == None):
            if check_password(data["password"], userInstance.password):
                rand_key = uuid4()
                tokenInstance = token.objects.create(
                    key=rand_key,
                    user_id=userInstance.id,
                    expiration_date=((3600*24*30) + time.time())
                )
                tokenInstance.save()
                response['Set-Cookie'] = 'utoken=' + str(tokenInstance.key) + "; Domain=" + settings.DOMAIN + "; Path=/; HttpOnly; SameSite=Strict"
                serializer = userSafeSerializer(userInstance)
                response.data = serializer.data
                print(response.data)
                response.status = status.HTTP_201_CREATED
                return response
        response.status = status.HTTP_400_BAD_REQUEST
        response.data = json.dumps({'status': 'email or password are incorrect!'})
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

    def get(self, request):
        users = user.objects.all()
        serializer = userSerializer(users, many=True)
        response = Response(serializer.data)
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        return response

    def post(self, request):
        print(request.POST.dict())
        data = request.POST.dict()
        print(data)
        operation = data["operation"]
        cookies = getCookies(request)
        uToken = cookies('utoken')
        if not (uToken == None) and not (uToken == ""):
            if operation == "logout":
                return self.logOut(uToken)
            else:
                response = Response()
                response['Access-Control-Allow-Origin'] = settings.HOST
                response['Access-Control-Allow-Credentials'] = 'true'
                tokenInstance = token.objects.get(key = uToken)
                userInstance = user.objects.get(id = tokenInstance.user_id)
                dict_obj = model_to_dict(userInstance)
                response.data = json.dumps(dict_obj)
                response.status = status.HTTP_201_CREATED
                return response
        else:
            print(data)
            query = QueryDict(data["data"]).dict()
            print(query)
            if operation == "signup":
                return self.signUp(query)
            elif operation == "login":
                return self.login(query)
        

    def put(self, request, id):
        snippet = user.objects.get(id=id)
        serializer = userSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

