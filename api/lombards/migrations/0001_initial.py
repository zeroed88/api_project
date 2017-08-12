# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 21:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PercentQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('percent', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Процент')),
                ('lastName', models.CharField(max_length=85, verbose_name='Фамилия')),
                ('zalogNumber', models.IntegerField(verbose_name='Номер ЗБ')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='ip')),
                ('serverAnswer', models.TextField(verbose_name='Ответ сервера')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Запрос процентов',
                'verbose_name_plural': 'Запросы процентов',
                'db_table': 'percents_queries',
            },
        ),
    ]
