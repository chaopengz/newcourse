# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 03:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20160712_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='created',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='chat',
            name='message',
            field=models.CharField(max_length=500),
        ),
    ]