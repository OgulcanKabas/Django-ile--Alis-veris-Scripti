# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import *
app_name = "home"

urlpatterns = [
    url('', index, name='index'),

]
