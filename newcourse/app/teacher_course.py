# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb,json
from models import *
import datetime, calendar
from django import forms
import os, tempfile, zipfile
from django.http import HttpResponse
from wsgiref.util import FileWrapper
# Create your views here.


class CourseShow:
    def __init__(self,course,isrun):
        self.course=course
        self.isrun=isrun

# 比较课程的起止日期与系统当前日期，从而返回该课程是否已经结束
def compare_time(time1,time2):
    nowtime=datetime.date.today()
    print (time2-nowtime).days
    if (nowtime - time1).days > 0 and (time2-nowtime).days>0:
        return True
    else:
        return False

def course_teacher_info(request, courseId):
     page_name = '课程详情'
     links=[{'name': '课程管理', 'page': '/teacher/course/'} ]
     request.session['course_id'] = courseId
     user=User.objects.filter(name=request.session['name']).first()
     course=Course.objects.filter(id=courseId).first()
     teacher=User.objects.filter(id=course.teacher_id).first()
     term=Term.objects.filter(id=course.term_id).first()
     isrun=compare_time(course.start_date, course.end_date)
     res = CourseShow(course,isrun)
     return render_to_response('teacher_course.html', locals())


def course_resource(request):
    list_num = 2
    page_name = '资源列表'
    links = [{'name': '课程管理', 'page': '/teacher/course'}, {'name': '资源管理', 'page': '/teacher/course/resource'}]
    user = User.objects.filter(name=request.session['name']).first()
    course_id = int(request.session['course_id'])
    user = User.objects.filter(name=request.session['name']).first()
    resource_classes = ResourceClass.objects.all()
    resources = Resource.objects.filter(course_id=course_id)
    return render_to_response('teacher_course_resource.html', locals())

class UserForm(forms.Form):
    Description = forms.CharField(label='资源名称')
    File = forms.FileField(label='文件位置')

def course_resource_publish(request):
    list_num = 2
    user = User.objects.filter(name=request.session['name']).first()
    page_name = '资源列表'
    links = [{'name': '课程管理', 'page': '/teacher/course'}, {'name': '资源管理', 'page': '/teacher/course/resource'},
             {'name': '发布资源', 'page': '/teacher/course/resource/resource_publish'} ]
    course_id = int(request.session['course_id'])
    resources = Resource.objects.filter(course_id=course_id)
    user=User.objects.filter(name=request.session['name']).first()
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            # 获取表单信息
            description = uf.cleaned_data['Description']
            filepath = uf.cleaned_data['File']
            # 写入数据库
            resource = Resource()
            resource_class = ResourceClass.objects.get(pk=1)
            resource.name = description
            resource.server_path = filepath
            resource.resource_class = resource_class
            resource.course_id = course_id
            resource.save()

            course_id = int(request.session['course_id'])
            resources = Resource.objects.filter(course_id=course_id)
            return HttpResponseRedirect('/teacher/course/resource/')
    else:
        uf = UserForm()

    return render_to_response('teacher_course_resource_publish.html', locals())


def course_resource_class(request):
    id = request.POST['resource_id']
    resource_class_id = request.POST['resource_class']
    resource = Resource.objects.get(pk=id)
    resource_class = ResourceClass.objects.get(pk=resource_class_id)
    resource.resource_class = resource_class
    resource.save()
    return HttpResponse(json.dumps(True))


def course_resource_class_add(request):
    name = request.POST['resource_class_name']
    resource_class = ResourceClass()
    resource_class.name = name
    resource_class.save()
    return HttpResponse(json.dumps(True))


def course_task(request):
     list_num = 1
     page_name = '作业列表'
     links=[{'name': '课程管理', 'page': '/teacher/course'} , {'name': '作业管理', 'page': '/teacher/course/task'}]
     user=User.objects.filter(name=request.session['name']).first()
     course_id=int(request.session['course_id'])
     tasks=TaskRequirement.objects.filter(course_id=course_id)
     return render_to_response('teacher_course_task.html', locals())


def course_task_publish(request):
     list_num = 1
     page_name = '作业列表'
     links=[{'name': '课程管理', 'page': '/teacher/course'} ,{'name': '作业管理', 'page': '/teacher/course/task'} ,
            {'name': '作业提交', 'page': '/teacher/course/task_publish'}]
     if request.method=='GET':
        user=User.objects.filter(name=request.session['name']).first()
        course_id=int(request.session['course_id'])
        return render_to_response('teacher_course_task_publish.html', locals())
     else:
        task = TaskRequirement()
        task.name = request.POST['name']
        task.base_requirements = request.POST['requirements']
        course_id = int(request.session['course_id'])
        course = Course.objects.filter(id=course_id).first()
        task.is_single = course.is_single
        task.course = course
        start = request.POST['start']
        end = request.POST['end']
        start_m = start[0:2]
        start_d = start[3:5]
        start_y = start[6:]
        end_m = end[0:2]
        end_d = end[3:5]
        end_y = end[6:]
        task.start_date =start_y + '-' + start_m + '-' + start_d
        task.end_date = end_y + '-' + end_m + '-' + end_d
        task.save()
        return HttpResponseRedirect('/teacher/course/task')


def course_task_info(request, task_id):
     list_num = 1
     page_name = '作业列表'
     links = [{'name': '课程管理', 'page': '/teacher/course'} ,{'name': '作业管理', 'page': '/teacher/course/task'} ,
              {'name': '作业详情', 'page': '/teacher/course/task_info'}]
     user = User.objects.filter(name=request.session['name']).first()
     course_id = int(request.session['course_id'])
     course=Course.objects.filter(id=course_id).first()
     teacher=User.objects.filter(id=course.teacher_id).first()
     term=Term.objects.filter(id=course.term_id).first()
     task = TaskRequirement.objects.get(pk=task_id)
     task_file =task.taskfile_set.all()
     request.session['task_id'] = task_id
     return render_to_response('teacher_course_task_info.html', locals())

def course_task_grade(request):
    id = request.POST['task_id']
    grade = request.POST['grade']
    task_file = TaskFile.objects.get(pk=id)
    task_file.grade=grade
    task_file.save()
    return HttpResponse(json.dumps(True))


def course_task_comment(request):
    id = request.POST['task_id']
    commnet = request.POST['comment']
    task_file = TaskFile.objects.get(pk=id)
    task_file.comment = commnet
    task_file.save()
    return HttpResponse(json.dumps(True))


def course_task_content(request):
    id = request.POST['task_id']
    task_file = TaskFile.objects.get(pk=id)
    return HttpResponse(json.dumps(task_file.content))


def one_click_download(request):
    """
    Create a ZIP file on disk and transmit it in chunks of 8KB,
    without loading the whole file into memory. A similar approach can
    be used for large dynamic PDF files.
    """
    filename = '1.doc'
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    archive.write(filename)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    user = User.objects.filter(name=request.session['name']).first()
    course_id = int(request.session['course_id'])
    task_id = request.session['task_id']
    return response


def file_download(request, filename):
        f = open(filename)
        data = f.read()
        f.close()
        response = HttpResponse(data)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response