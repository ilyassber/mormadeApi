from django.shortcuts import render
from django.conf import settings
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
from .. models.tag import tag
from .. serializers.articleSerializer import articleSerializer
from .. serializers.contentSerializer import contentSerializer
from .. serializers.imageSerializer import imageSerializer
from .. services.api.getCookies import getCookies
from .. serializers.tagSerializer import tagSerializer

class articleViewStd(APIView):

    def getImageById(self, id):
        imageInstance = image.objects.filter(id=id)
        print(imageInstance)
        if len(imageInstance) == 0:
            return None
        serializer = imageSerializer(imageInstance[0])
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

    def getArticles(self, id):
        if id == None:
            data = article.objects.all()
        else :
            data = article.objects.filter(id=id)
        serializer = articleSerializer(data, many=True)
        articles = serializer.data
        print(articles)
        for a in articles:
            a['cover'] = self.getImageById(a['cover'])
            a['text'] = self.getTextContent(a['text'])
        return articles

    def getTrendingArticles(self):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        data = article.objects.filter(trending=True)
        serializer = articleSerializer(data, many=True)
        articles = serializer.data
        for a in articles:
            a['cover'] = self.getImageById(a['cover'])
            a['text'] = self.getTextContent(a['text'])
        response.data = articles
        response.status = status.HTTP_200_OK
        return response

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

    def registerArticle(self, data, utoken):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        if not (utoken == None) and not (utoken == ""):
            tokenInstance = token.objects.get(key = utoken)
            if not (tokenInstance == None) and (tokenInstance.expired == False):
                userInstance = user.objects.get(id = tokenInstance.user_id)
                if not (userInstance == None):
                    print(userInstance.id)
                    contents = QueryDict(data['text']).dict().values()
                    data['text'] = []
                    serializer = articleSerializer(data = data)
                    if serializer.is_valid():
                        articleInstance = serializer.save()
                        articleInstance.author_id = userInstance.id
                        articleInstance.url = str(articleInstance.id) + '-' + articleInstance.title.replace(" ", "-")
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
    
    def getAll(self):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        response.data = self.getArticles(None)
        response.status = status.HTTP_200_OK
        return response

    def getById(self, id):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        response.data = self.getArticles(id)
        response.status = status.HTTP_200_OK
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
        return self.getAll()

    def post(self, request):
        data = request.POST.dict()
        cookies = getCookies(request)
        utoken = cookies('utoken')
        if data["operation"] == "register":
            print(QueryDict(data["data"]).dict())
            return self.registerArticle(QueryDict(data["data"]).dict(), utoken)
        elif data["operation"] == "all":
            return self.getAll()
        elif data["operation"] == "get":
            return self.getById(int(data["id"]))
        elif data["operation"] == "trending":
            return self.getTrendingArticles()
        else :
            response = Response()
            response['Access-Control-Allow-Origin'] = settings.HOST
            response['Access-Control-Allow-Credentials'] = 'true'
            response.data = "Baaad idea !O_o!"
            response.status = status.HTTP_400_BAD_REQUEST
            return response


class articleViewId(APIView):

    def getImageById(self, id):
        imageInstance = image.objects.filter(id=id)
        if len(imageInstance) == 0:
            return None
        serializer = imageSerializer(imageInstance[0])
        return serializer.data

    def getTags(self, list):
        tags = []
        if list != None and len(list) > 0:
            for n in list:
                tagInstance = tag.objects.get(id=n)
                print(tagInstance)
                serializer = tagSerializer(tagInstance)
                tags.append(serializer.data)
        return tags

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

    def getArticle(self, id):
        data = article.objects.filter(id=id)
        serializer = articleSerializer(data, many=True)
        articleInstance = serializer.data[0]
        print(articleInstance)
        articleInstance['cover'] = self.getImageById(articleInstance['cover'])
        articleInstance['text'] = self.getTextContent(articleInstance['text'])
        articleInstance['tags'] = self.getTags(articleInstance['tags'])
        return articleInstance

    def options(self, request):
        response = Response()
        response['Allow'] = 'GET, POST, PUT, HEAD, OPTIONS'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, HEAD, OPTIONS'
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Request-Method'] = 'GET, POST'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, X-CSRFToken, Access-Control-Request-Method, Access-Control-Request-Headers'
        return response

    def get(self, request, id):
        response = Response()
        response['Access-Control-Allow-Origin'] = settings.HOST
        response['Access-Control-Allow-Credentials'] = 'true'
        response.data = self.getArticle(id)
        response.status = status.HTTP_200_OK
        return response