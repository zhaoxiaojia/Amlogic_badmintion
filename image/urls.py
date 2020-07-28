# encoding:utf-8
from django.urls import path
from django.conf.urls import url, include

from . import views
from .views import ImageList

urlpatterns = [
    url(r'^list_image/$', ImageList.as_view(), name='list_image'),
    url(r'^upload_image/$', views.upload_image, name='upload_image'),
    url(r'^del_image/$', views.del_image, name='del_image'),
    url(r'^fall_image/$', views.falls_images, name='fall_image'),
]
