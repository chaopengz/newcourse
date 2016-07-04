# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-04 11:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('introduction', models.CharField(max_length=300)),
                ('is_single', models.BooleanField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('is_allowed', models.BooleanField()),
                ('max_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GroupCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_allowed', models.BooleanField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Course')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('publish_date', models.DateField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('directory', models.CharField(max_length=500)),
                ('server_path', models.FilePathField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Course')),
            ],
        ),
        migrations.CreateModel(
            name='TaskFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('submit_time', models.DateTimeField()),
                ('content', models.CharField(max_length=300)),
                ('group_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TaskRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('base_requirements', models.CharField(max_length=300)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_single', models.BooleanField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('week', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_allowed', models.BooleanField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User')),
            ],
        ),
        migrations.AddField(
            model_name='taskfile',
            name='task_requirement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.TaskRequirement'),
        ),
        migrations.AddField(
            model_name='taskfile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User'),
        ),
        migrations.AddField(
            model_name='course',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Term'),
        ),
    ]
