"""ecomartapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from webapi.views import productView
from webapi.views.userView import userView
from webapi.views.imageView import imageView
from webapi.views.tagView import tagView
from webapi.views.articleView import articleViewStd, articleViewId
from webapi.views.messageView import messageView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/products/', productView.productList.as_view()),
    path('api/products/<int:id>', productView.productOps.as_view()),
    path('api/users/', userView.as_view()),
    path('api/images/<int:id>', imageView.as_view()),
    path('api/images/', imageView.as_view()),
    path('api/categories/', tagView.as_view()),
    path('api/articles/', articleViewStd.as_view()),
    path('api/articles/<int:id>', articleViewId.as_view()),
    path('api/messages/', messageView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
