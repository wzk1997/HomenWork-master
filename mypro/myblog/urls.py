"""mypro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'myblog'
urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^login', views.login, name='login'),
    url(r'^register/', views.regist, name='register'),
    url(r'^lastpwd/',views.lastpwd,name='lastpwd'),
    url(r'^index1/',views.index1,name='index1'),
    url(r'^article/',views.article,name='article'),
    url(r'^article_detele/',views.article_detele,name='article_detele'),
    url(r'^updata_article/',views.updata_article,name='updata_article'),
    url(r'^article_list/',views.article_list,name='article_list'),
    url(r'^addutils/',views.addutils,name='addutils'),
    url(r'^jsontext/',views.jsontext,name='jsontext'),

]
