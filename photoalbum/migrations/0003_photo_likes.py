# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-29 08:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photoalbum', '0002_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
