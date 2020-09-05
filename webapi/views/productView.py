from django.shortcuts import render
import json

from django.http import HttpResponse
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .. models.product import product
from .. models.token import token
from .. models.user import user
from .. models.image import image
from .. serializers.productSerializer import productSerializer
from .. serializers.imageSerializer import imageSerializer
from .. services.api.getCookies import getCookies

class productList(APIView):

    def getProductImagesJson(self, product):
        idsList = product.pics_list
        images = []
        for i in idsList:
            images.append(image.objects.get(id=i))
        serializer = imageSerializer(images, many=True)
        return serializer.data

    def getProductByToken(self, uToken):
        tokenInstance = token.objects.get(key=uToken)
        userInstance = user.objects.get(id=tokenInstance.user_id)
        products = product.objects.filter(maker_id=userInstance.id)
        for p in products:
            p.images = self.getProductImagesJson(p)
        return products

    def options(self, request):
        response = Response()
        response['Allow'] = 'GET, POST, PUT, HEAD, OPTIONS'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, HEAD, OPTIONS'
        response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response['Access-Control-Request-Method'] = 'GET, POST'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, X-CSRFToken, Access-Control-Request-Method, Access-Control-Request-Headers'
        return response

    def get(self, request):
        response = Response()
        response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response['Access-Control-Allow-Credentials'] = 'true'
        cookies = json.loads(str(request.COOKIES).replace("\'", "\""))
        uToken = None
        if 'utoken' in cookies:
            uToken = cookies["utoken"]
            products = self.getProductByToken(uToken)
            serializer = productSerializer(products, many=True)
            response.data = serializer.data
            response.status = status.HTTP_200_OK
            print(uToken)
        else:
            print("No cookies!")
            response.data = 'No products'
            response.status = status.HTTP_200_OK
        return response

    def post(self, request):
        response = Response()
        response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response['Access-Control-Allow-Credentials'] = 'true'
        cookies = getCookies(request)
        utoken = cookies('utoken')
        if not (utoken == None) and not (utoken == ""):
            tokenInstance = token.objects.get(key = utoken)
            if not (tokenInstance == None) and (tokenInstance.expired == False):
                userInstance = user.objects.get(id = tokenInstance.user_id)
                if not (userInstance == None):
                    data = request.POST.dict()
                    query = QueryDict(data["data"]).dict()
                    print(query)
                    pics = QueryDict(query['pics_list']).dict().values()
                    print(pics)
                    query['pics_list'] = pics
                    print(query)
                    serializer = productSerializer(data = query)
                    if serializer.is_valid():
                        productInstance = serializer.save()
                        productInstance.maker_id = userInstance.id
                        productInstance.maker_name = userInstance.username
                        productInstance.save()
                        response.data = serializer.data
                        response.status = status.HTTP_201_CREATED
                        return response
                    else:
                        response.data = serializer.errors
                        response.status = status.HTTP_400_BAD_REQUEST
                        return response
                else:
                    response.data = 'user not exist'
                    response.status = status.HTTP_400_BAD_REQUEST
                    return response
            else:
                response.data = 'token not exist or expired'
                response.status = status.HTTP_400_BAD_REQUEST
                return response
        else:
            response.data = 'token not valid'
            response.status = status.HTTP_400_BAD_REQUEST
            return response

    def put(self, request, id):
        snippet = product.objects.get(id=id)
        serializer = productSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class productOps(APIView):

    def put(self, request, id):
        snippet = product.objects.get(id=id)
        serializer = productSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)