# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2021-06-30 12:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adi', models.CharField(max_length=50)),
                ('aktif_mi', models.BooleanField(default=True, verbose_name='Aktif mi')),
            ],
        ),
        migrations.CreateModel(
            name='Urunler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urun_adi', models.CharField(max_length=150, null=True, verbose_name='Oyun ismi')),
                ('urun_aciklama', models.TextField(max_length=2000, null=True, verbose_name='Oyun a\xe7\u0131klama ')),
                ('birim_fiyat', models.FloatField(null=True, verbose_name='Birim Fiyat ')),
                ('resim', models.ImageField(null=True, upload_to='images/', verbose_name='Foto\u011fraf')),
                ('kategori', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Kategori')),
            ],
            options={
                'verbose_name': '\xdcrun',
                'verbose_name_plural': '\xdcr\xfcnler',
            },
        ),
    ]
