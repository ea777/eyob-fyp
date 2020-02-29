from django.conf.urls import url
from .views import *
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from . import views
admin.autodiscover()
urlpatterns = [

    url(r'^$', views.index, name='index'),

    path('shop_table/<str:id>', views.shop_table, name='shop_table'),
    path('shop_chart/<str:id>', views.shop_chart, name='shop_chart'),



]
