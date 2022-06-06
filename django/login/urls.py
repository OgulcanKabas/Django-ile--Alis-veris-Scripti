
# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from .views import *
app_name = "login"

urlpatterns = [
    url(r'^giris/$', giris_view, name='giris'),
    url(r'^kayit/$', kayit_view, name="kayit"),
    url(r'^cikis/$', cikis_view, name="cikis"),
    url(r'^sepet/$', sepet_view, name="sepet"),
    url(r'^index/(?P<id>\w+)/$', index_filtre, name='index_filtre'),


]