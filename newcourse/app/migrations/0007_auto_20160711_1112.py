# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-11 03:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20160708_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='number',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='chat',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
