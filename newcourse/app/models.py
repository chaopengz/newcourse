# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    type = models.IntegerField()
    real_name = models.CharField(max_length=30)
    pic = models.CharField(max_length=50, default='none')


class Term(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    week = models.IntegerField()


class Group(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey('User')  # 团队负责人
    max_number = models.IntegerField()
    end = models.IntegerField(default=1)  # 1代表目前还可以申请加入


class Course(models.Model):
    name = models.CharField(max_length=30)
    introduction = models.CharField(max_length=300)
    is_single = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()
    term = models.ForeignKey('Term')
    teacher = models.ForeignKey('User')


def get_resource_path(instance, filename):
    course_id = instance.course.id
    return 'resource/' + str(course_id) + '/' + filename


class ResourceClass(models.Model):
    name = models.CharField(max_length=30)


class Resource(models.Model):
    name = models.CharField(max_length=30)
    server_path = models.FileField(upload_to=get_resource_path)
    resource_class = models.ForeignKey('ResourceClass')
    course = models.ForeignKey('Course')
    submit_time = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    content = models.CharField(max_length=300)
    publish_date = models.DateField()
    course = models.ForeignKey('Course')
    user = models.ForeignKey('User')


def get_task_file_path(instance, filename):
    user_id = instance.user.id
    task_id = instance.task_requirement.id
    course_id = instance.task_requirement.course.id
    return 'task/' + str(course_id) + '/' + str(task_id) + '/' + str(user_id) + '/' + filename


class TaskRequirement(models.Model):
    name = models.CharField(max_length=30)
    base_requirements = models.CharField(max_length=300)
    start_date = models.DateField()
    end_date = models.DateField()
    is_single = models.BooleanField()
    course = models.ForeignKey('Course')


class TaskFile(models.Model):
    name = models.CharField(max_length=300)
    submit_time = models.DateTimeField(auto_now_add=True)
    is_file = models.BooleanField(default=False)
    content = models.CharField(max_length=300)
    server_path = models.FileField(upload_to=get_task_file_path, default='/task')
    grade = models.IntegerField(default=0)
    comment = models.CharField(max_length=300, default='')
    task_requirement = models.ForeignKey('TaskRequirement')
    user = models.ForeignKey('User')
    group_id = models.IntegerField()


class UserCourse(models.Model):
    user = models.ForeignKey('User')
    course = models.ForeignKey('Course')


class UserGroup(models.Model):
    user = models.ForeignKey('User')
    group = models.ForeignKey('Group')
    is_allowed = models.IntegerField(default=0)


class GroupCourse(models.Model):
    group = models.ForeignKey('Group')
    course = models.ForeignKey('Course')
    is_allowed = models.BooleanField()


class Chat(models.Model):
    created = models.DateTimeField()
    user = models.ForeignKey('User')
    message = models.CharField(max_length=200)
    courseid = models.IntegerField(default=0)

    def __unicode__(self):
        return self.message
