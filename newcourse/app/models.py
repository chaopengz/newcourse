from __future__ import unicode_literals

from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    type = models.IntegerField()


class Term(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    week = models.IntegerField()


class Group(models.Model):
    name = models.CharField(max_length=30)
    is_allowed = models.BooleanField()
    max_number = models.IntegerField()


class Course(models.Model):
    name = models.CharField(max_length=30)
    introduction = models.CharField(max_length=300)
    is_single = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()
    term = models.ForeignKey('Term')
    teacher = models.ForeignKey('User')


class Resource(models.Model):
    name = models.CharField(max_length=30)
    directory = models.CharField(max_length=500)
    server_path = models.FilePathField()
    course = models.ForeignKey('Course')


class Message(models.Model):
    content = models.CharField(max_length=300)
    publish_date = models.DateField()
    course = models.ForeignKey('Course')
    user = models.ForeignKey('User')


class TaskRequirement(models.Model):
    name = models.CharField(max_length=30)
    base_requirements = models.CharField(max_length=300)
    start_date = models.DateField()
    end_date = models.DateField()
    is_single = models.BooleanField()
    course = models.ForeignKey('Course')


class TaskFile(models.Model):
    name = models.CharField(max_length=300)
    submit_time = models.DateTimeField()
    is_file = models.BooleanField(default=False)
    content = models.CharField(max_length=300)
    task_requirement = models.ForeignKey('TaskRequirement')
    user = models.ForeignKey('User')
    group_id = models.IntegerField()


class UserCourse(models.Model):
    user = models.ForeignKey('User')
    course = models.ForeignKey('Course')


class UserGroup(models.Model):
    user = models.ForeignKey('User')
    group = models.ForeignKey('Group')
    is_allowed = models.BooleanField()


class GroupCourse(models.Model):
    group = models.ForeignKey('Group')
    course = models.ForeignKey('Course')
    is_allowed = models.BooleanField()
