# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-26 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lombards', '0004_auto_20161014_1034'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, verbose_name='Имя')),
                ('address', models.TextField(max_length=400, verbose_name='Адрес')),
                ('phone', models.CharField(max_length=11, verbose_name='Телефон')),
                ('shop', models.BooleanField(default=False, verbose_name='Магазин')),
                ('image', models.ImageField(upload_to='filials', verbose_name='Изображение')),
                ('start_time', models.TimeField(verbose_name='Начало работы')),
                ('end_time', models.TimeField(verbose_name='Окончание работы')),
                ('long', models.FloatField(default=0.0, verbose_name='Longitude(долгота)')),
                ('lat', models.FloatField(default=0.0, verbose_name='Latitude(широта)')),
            ],
        ),
    ]