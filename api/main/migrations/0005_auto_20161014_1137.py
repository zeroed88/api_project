# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-14 08:37
from __future__ import unicode_literals

from django.db import migrations
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20161014_1036'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', main.models.UserManager()),
            ],
        ),
    ]