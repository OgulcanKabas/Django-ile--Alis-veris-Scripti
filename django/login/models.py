# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class KullaniciBilgi(models.Model):
    kullanici = models.OneToOneField(User, on_delete=models.CASCADE)
    adi = models.CharField ( max_length = 150,verbose_name='Ad',null=True)
    soyadi = models.CharField ( max_length = 150,verbose_name='Soyad',null=True)
    dogum_tarihi = models.DateTimeField(auto_now_add=False,verbose_name='Dogum Tarihi',null=True)
    cinsiyet = models.CharField (max_length = 30,verbose_name='Cinsiyet ',null=True)
    def __unicode__(self):
        return "{}".format(self.adi)

    def __str__(self):
        return self.__unicode__()