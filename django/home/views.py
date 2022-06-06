# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render,redirect

from django.http import HttpResponse
from home.models import *
from login.models import *
from django.contrib.auth import authenticate, login, logout

def index(request): #Url fonksiyonunu oluşturuyoruz
    post = request.POST #Post değerlerini alıyoruz
    alert = "" #Boş değişken tanımlıyoruz
    kullanici_profili = None #boş değişken tanımlıyoruz
    if request.user.is_authenticated: #Kullanıcı giriş yapmış mı ?
        kullanici_profili = KullaniciBilgi.objects.filter(kullanici=request.user).first() #Yaptıysa bilgileri alıyoruz
    sepet = None
    if kullanici_profili: #Eğer kullanıcı giriş yaptıysa
        if post: #Ve gelen istek post işlemiyse
            adet = int(post.get("adet",0)) #Adeti alıyoruz
            urun_id = post.get("urun_id") #Urun id değerini alıyoruz.
            urun = Urunler.objects.filter(id=urun_id).first() #Ürünler tablosunda aratıyoruz.
            if adet <=0: #Adet sıfırdan küçük veya eşitse alert ekliyoruz.
                alert = "Adet Sıfır Olamaz!"
            else:#Değilse devam ediyoruz.
                yeni_sepet = Sepet.objects.filter(kullanici=kullanici_profili,urun=urun,aktif_mi=True).first() 
                #Eğer kullanıcının o ürüne ait aktif sepeti varsa onu alıyoruz ve adeti güncelliyoruz.
                if yeni_sepet:
                    adet += yeni_sepet.adet
                else:#eğer yoksa yeni sepet nesnesi oluşturuyoruz.
                    yeni_sepet = Sepet()
                yeni_sepet.adet = adet
                yeni_sepet.kullanici = kullanici_profili
                yeni_sepet.urun = urun
                yeni_sepet.save() #Değerleri atayıp save işlemi yapıyoruz.
                #Eklendiğinin bilgisini veriyoruz.
                #ve ürünler, kategoriler listesiyle tüm değerleri yeniden sayfaya gönderiyoruz.
                alert = "{} {} Adet Ürün Sepete Eklenmiştir.".format(urun.urun_adi, int(post.get("adet",0))) 
        sepet = Sepet.objects.filter(kullanici=kullanici_profili,aktif_mi=True).count()
    if post and not kullanici_profili:
        alert = "Sepete Ürün Eklemek İçin, Giriş Yapmalısınız!"
    urunler = Urunler.objects.filter()
    kategoriler = Kategori.objects.filter(aktif_mi=True)

    context = {
        "urunler":urunler,
        "sepet_urun_sayisi":sepet,
        "alert":alert,
        "kategoriler":kategoriler
    }
    return render(request, "index.html", context)

