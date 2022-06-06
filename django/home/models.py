# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from login.models import KullaniciBilgi

# Create your models here.
class Kategori(models.Model):
    adi = models.CharField(max_length=50)
    aktif_mi = models.BooleanField(default=True,verbose_name='Aktif mi')

    def __unicode__(self):
        return "{}".format(self.adi)

    def __str__(self):
        return self.__unicode__()

class Urunler(models.Model):
    urun_adi = models.CharField ( max_length = 150,verbose_name='Ürün ismi',null=True)
    urun_aciklama = models.TextField( max_length = 2000,verbose_name='Ürün açıklama ',null=True)
    birim_fiyat = models.FloatField(verbose_name='Birim Fiyat ',null=True)
    resim = models.ImageField(null=True,verbose_name='Fotoğraf',upload_to='images/')
    kategori = models.ForeignKey(
        'Kategori',
        on_delete=models.CASCADE,
        null=True
        )
   
    def __unicode__(self):
        return "{}".format(self.urun_adi)

    def __str__(self):
        return self.__unicode__()

    def get_image_path(self):
        return self.resim
    
    class Meta:
        verbose_name = 'Ürun'
        verbose_name_plural = 'Ürünler'


class Sepet(models.Model):
    urun = models.ForeignKey('Urunler', on_delete=models.CASCADE, null=True)
    adet = models.IntegerField(verbose_name='Adet ',null=True)
    kullanici = models.ForeignKey(KullaniciBilgi, on_delete=models.CASCADE, null=True)
    aktif_mi = models.BooleanField(default=True,verbose_name='Aktif mi')

    def __unicode__(self):
        return "{}".format(self.urun.urun_adi)

    def __str__(self):
        return self.__unicode__()
    
    class Meta:
        verbose_name = 'Sepet'
        verbose_name_plural = 'Sepetler'

class Satilanlar(models.Model):
    sepet = models.ManyToManyField('Sepet')
    genel_total = models.CharField(max_length=10, verbose_name='Total ',null=True)
    satilma_tarihi = models.DateField(auto_now_add=True, verbose_name='Oyun çıkış tarihi',null=True)

    def __unicode__(self):
        return "satış "

    def __str__(self):
        return self.__unicode__()
    class Meta:
        verbose_name = 'Satış'
        verbose_name_plural = 'Satılanlar'