# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from login.models import KullaniciBilgi



class GirisForm(forms.Form):
    kullanici_adi = forms.CharField(max_length=100, label='Kullanıcı Adı', widget=forms.TextInput(attrs={"class":"form-control text-center","placeholder":"Kullanıcı Adı"}))
    sifre = forms.CharField(max_length=100, label='Şifre', widget=forms.PasswordInput(attrs={"class":"form-control text-center","placeholder":"Şifre"}))

    def clean(self):
        username = self.cleaned_data.get('kullanici_adi')
        password = self.cleaned_data.get('sifre')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Kullanıcı adını veya şifreyi yanlış girdiniz!")
        return super(GirisForm, self).clean()

class KayitForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label='Kullanıcı Adı', widget=forms.TextInput(attrs={"class":"form-control text-center","placeholder":"Kullanıcı Adı"}))
    password1 = forms.CharField(max_length=100,label='Parola', widget=forms.PasswordInput(attrs={"class":"form-control text-center","placeholder":"Şifre"}))
    password2 = forms.CharField(max_length=100, label='Parola Doğrulama', widget=forms.PasswordInput(attrs={"class":"form-control text-center","placeholder":"Şifre(Tekrar)"}))
    ad = forms.CharField(max_length=100, label='Adınız', widget=forms.TextInput(attrs={"class":"form-control text-center","placeholder":"Adınız"}))
    soyad = forms.CharField(max_length=100, label='Soyadınız', widget=forms.TextInput(attrs={"class":"form-control text-center","placeholder":"Soyadınız"}))
    yas = forms.CharField(label='Doğum Tarihi', widget=forms.widgets.DateTimeInput(attrs={"type": "date","class":"form-control text-center"}))

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'ad',
            'soyad',
            'yas'
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Şifreler Eşleşmiyor!")
        return super(KayitForm, self).clean()



