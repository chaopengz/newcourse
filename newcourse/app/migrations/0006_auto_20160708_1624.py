# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-08 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_group_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupcourse',
            name='is_allowed',
            field=models.IntegerField(default=0),
        ),
    ]