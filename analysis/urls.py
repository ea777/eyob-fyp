from django.conf.urls import url
from .views import *
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from . import views
admin.autodiscover()
urlpatterns = [

    url(r'^$', views.index, name='index'),



]