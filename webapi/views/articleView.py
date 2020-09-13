from django.shortcuts import render
import json

from django.http import HttpResponse
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .. models.article import article
from .. models.content import content
from .. models.token import token
from .. models.user import user
from .. models.image import image
from .. serializers.articleSerializer import articleSerializer
from .. serializers.contentSerializer import contentSerializer
from .. serializers.imageSerializer import imageSerializer
from .. services.api.getCookies import getCookies

class articleView(APIView):

    def getImageById(self, id):
        imageInstance = image.objects.get(id=id)
        serializer = imageSerializer(imageInstance)
        return serializer.data

    def getContentById(self, id):
        contentInstance = content.objects.get(id=id)
        serializer = contentSerializer(contentInstance)
        contentData = serializer.data
        if contentData['type'] == 'text':
            return contentData
        else:
            contentData['image'] = self.getImageById(contentData['image'])
            return contentData

    def getTextContent(self, list):
        textContent = []
        for i in list:
            textContent.append(self.getContentById(i))
        return textContent

    def getArticles(self):
        data = article.objects.all()
        serializer = articleSerializer(data, many=True)
        articles = serializer.data
        print(articles)
        for a in articles:
            a['cover'] = self.getImageById(a['cover'])
            a['text'] = self.getTextContent(a['text'])
        return articles

    def saveArticleContent(self, contents, article_id):
        idsList = []
        newContents = []
        for c in contents:
            c = QueryDict(c).dict()
            c['article_id'] = article_id
            newContents.append(c)
        for l in newContents:
            serializer = contentSerializer(data = l)
            if serializer.is_valid():
                contentInstance = serializer.save()
                idsList.append(contentInstance.id)
        return idsList

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
            response.data = self.getArticles()
            response.status = status.HTTP_200_OK
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
                    print(userInstance.id)
                    query = request.POST.dict()
                    contents = QueryDict(query['text']).dict().values()
                    query['text'] = []
                    serializer = articleSerializer(data = query)
                    if serializer.is_valid():
                        articleInstance = serializer.save()
                        articleInstance.author_id = userInstance.id
                        articleInstance.text = self.saveArticleContent(contents, articleInstance.id)
                        articleInstance.save()
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