# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 02:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20160711_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='created',
            field=models.DateTimeField(),
        ),
    ]
