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

    def signUp(self, data, operation):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        is_exist = user.objects.filter(email = data["email"]).count()
        if is_exist == 0:
            if operation == "signup":
                hashedPassword = make_password(data["password"])
                data["password"] = hashedPassword
            serializer = userSerializer(data = data)
            response = Response()
            if serializer.is_valid():
                userInstance = serializer.save()
                rand_key = uuid4()
                if operation == "signup":
                    tokenInstance = token.objects.create(
                        key=rand_key,
                        user_id=userInstance.id,
                        expiration_date=((3600*24*30) + time.time())
                    )
                    tokenInstance.save()
                    response['Set-Cookie'] = 'utoken=' + str(tokenInstance.key)+ "; Domain=" + settings.DOMAIN + "; Max-Age=31104000; Path=/; HttpOnly; SameSite=Strict"
                    print(tokenInstance.key)
                response.data = serializer.data
                print(response.data)
                response.status = status.HTTP_201_CREATED
                return response
            response.data = serializer.errors
            response.status = status.HTTP_400_BAD_REQUEST
            return response
        elif operation == "signup_maker":
            userInstance = user.objects.get(email=data["email"])
            userInstance.is_maker = True
            userInstance.save()
            response.data = json.dumps({'status': 'registred as maker!'})
            response.status = status.HTTP_201_CREATED
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
                response['Set-Cookie'] = 'utoken=' + str(tokenInstance.key) + "; Domain=" + settings.DOMAIN + "; Max-Age=31104000; Path=/; HttpOnly; SameSite=Strict"
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
        data = request.POST.dict()
        operation = data["operation"]
        cookies = getCookies(request)
        uToken = cookies('utoken')
        if (not (uToken == None) and not (uToken == "")) and (operation != "signup_maker"):
            if operation == "logout":
                return self.logOut(uToken)
            else:
                response = Response()
                response['Access-Control-Allow-Origin'] = settings.HOST
                response['Access-Control-Allow-Credentials'] = 'true'
                tokenInstance = token.objects.get(key = uToken)
                userInstance = user.objects.get(id = tokenInstance.user_id)
                serializer = userSafeSerializer(userInstance)
                response.data = serializer.data
                response.status = status.HTTP_201_CREATED
                return response
        else:
            query = QueryDict(data["data"]).dict()
            if operation == "signup" or operation == "signup_maker":
                return self.signUp(query, operation)
            elif operation == "login":
                return self.login(query)
            else:
                response = Response()
                response['Access-Control-Allow-Origin'] = settings.HOST
                response['Access-Control-Allow-Credentials'] = 'true'
                response.status = status.HTTP_400_BAD_REQUEST
                response.data = json.dumps({'status': 'Invalid!'})
                return response

