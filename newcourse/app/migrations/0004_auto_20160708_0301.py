# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20160708_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroup',
            name='is_allowed',
            field=models.IntegerField(default=0),
        ),
    ]
