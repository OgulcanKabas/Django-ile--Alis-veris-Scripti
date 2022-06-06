# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random

from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from login.forms import GirisForm, KayitForm
from home.models import *
from login.models import *

def giris_view(request):
    form = GirisForm(request.POST or None)
    if form.is_valid():
        kullanici_adi = form.cleaned_data.get('kullanici_adi')
        sifre = form.cleaned_data.get('sifre')
        yeni_giris = authenticate(username=kullanici_adi, password=sifre)
        login(request, yeni_giris)
        return redirect('/')
    return render(request, "girisYap.html", {"form": form})

def kayit_view(request):
    form = KayitForm(request.POST or None)
    if form.is_valid():
        kayit = form.save(commit=False)
        sifre = form.cleaned_data.get('password1')
        ad = form.cleaned_data.get('ad')
        soyad = form.cleaned_data.get('soyad')
        yas = form.cleaned_data.get('yas')
        kayit.set_password(sifre)
        # user.is_staff = user.is_superuser = True
        kayit.save()
        yeni_giris = authenticate(username=kayit.username, password=sifre)
        login(request, yeni_giris)
        kullanici_bilgi = KullaniciBilgi()
        kullanici_bilgi.kullanici = kayit
        kullanici_bilgi.dogum_tarihi = yas
        kullanici_bilgi.soyadi = soyad
        kullanici_bilgi.adi = ad
        kullanici_bilgi.cinsiyet = "Belirtilmedi"
        kullanici_bilgi.save()
        return redirect('/')
    return render(request, "kayitOl.html", {"form": form, 'title': 'Üye Ol'})

def cikis_view(request):
    logout(request)
    return redirect('/')


def sepet_view(request):
    post = request.POST
    kullanici_profili = None
    tavsiye_edilen = None
    if request.user.is_authenticated:
        kullanici_profili = KullaniciBilgi.objects.filter(kullanici=request.user).first()
    sepet = Sepet.objects.filter(kullanici=kullanici_profili,aktif_mi=True)#Kullanıcının aktif sepetlerini al

    if post and post.get("onay"):#Eğer post işlemi ve onay işlemiyse
        genel_total = post.get("genel_total") #Genel total'i al
        yeni_satis = Satilanlar() #Satilanlar tablosunun nesnesini oluştur
        yeni_satis.genel_total = genel_total #Genel Total'i yaz
        yeni_satis.save() #kaydet

        for sep in sepet: #Sepet sorgu listesini döngüye sokuyoruz.
            yeni_satis.sepet.add(sep) #Manytomany olan alana sepetleri ekliyoruz.
            yeni_satis.save()#kayıt ediyoruz.
            sep.aktif_mi = False #sepeti aktif değil olarak işaretliyor
            sep.save()# ve kayıt ediyoruz.
        return render(request, "satis_basarili.html", {}) #Döngü bittiği zaman satis_basarili sayfasına gönderiyoruz.
    if post:
        sepet_id = post.get("sepet_id")
        sepet = Sepet.objects.filter(id=int(sepet_id)).first()
        sepet.delete()
        return redirect('/kullanici/sepet/')
    data =  []
    genel_total = 0
    for row in sepet:
        total = float(row.urun.birim_fiyat) * float(row.adet)
        genel_total += total
        data.append({
            "sepet_id": row.id,
            "urun_adi": row.urun.urun_adi,
            "adet": row.adet,
            "birim_fiyat": row.urun.birim_fiyat,
            "total_tutar": total,
            "resim": row.urun.resim
        })

    context = {
        "data":data,
        "genel_total":genel_total,
        "sepet_urun_sayisi": len(sepet),
    }
    return render(request, "sepet.html", context)
def index_filtre(request, id=None):
    post = request.POST
    alert = ""
    kullanici_profili = None
    if request.user.is_authenticated:
        kullanici_profili = KullaniciBilgi.objects.filter(kullanici=request.user).first()
    sepet = None
    if kullanici_profili:
        if post:
            adet = int(post.get("adet",0))
            urun_id = post.get("urun_id")
            urun = Urunler.objects.filter(id=urun_id).first()
            if adet <=0:
                alert = "Adet Sıfır Olamaz!"
            else:
                yeni_sepet = Sepet.objects.filter(kullanici=kullanici_profili,urun=urun,aktif_mi=True).first()
                if yeni_sepet:
                    adet += yeni_sepet.adet
                else:
                    yeni_sepet = Sepet()
                yeni_sepet.adet = adet
                yeni_sepet.kullanici = kullanici_profili
                yeni_sepet.urun = urun
                yeni_sepet.save()
                alert = "{} {} Adet Ürün Sepete Eklenmiştir.".format(urun.urun_adi, int(post.get("adet",0)))
        sepet = Sepet.objects.filter(kullanici=kullanici_profili,aktif_mi=True).count()
    if post and not kullanici_profili:
        alert = "Sepete Ürün Eklemek İçin, Giriş Yapmalısınız!"
    urunler = Urunler.objects.filter(kategori_id=id)
    kategoriler = Kategori.objects.filter(aktif_mi=True)

    context = {
        "urunler":urunler,
        "sepet_urun_sayisi":sepet,
        "alert":alert,
        "kategoriler":kategoriler
    }
    return render(request, "index.html", context)