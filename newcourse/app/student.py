# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import loader, context, RequestContext
import MySQLdb
from models import *
from django import forms
import json

# Create your views here.
def student(request):
    links = [{'name': '学生页面', 'page': '/student/'}]
    if 'name' in request.session:
        name = request.session['name']
        user = User.objects.filter(name=name).first()
        if user is not None:
            return render_to_response('student.html', locals())
    return HttpResponseRedirect('/login/')


def student_info(request):
    links = [{'name': '学生页面', 'page': '/student/'}]
    list_num = 1
    user = User.objects.filter(name=request.session['name']).first()
    return render_to_response('student_info.html', locals())


def student_course(request):
    page_name = '课程列表'
    list_num = 2
    links = [{'name': '学生页面', 'page': '/student/'}]
    user = User.objects.filter(name=request.session['name']).first()
    # usercourses = UserCourse.objects.filter(user_id=user.id)
    usercourses = UserCourse.objects.filter(user_id=user.id)
    courses = []
    for usercourse in usercourses:
        courses.append(Course.objects.get(id=usercourse.course_id))
    course_teachers = []
    for course in courses:
        course_teachers.append([course, User.objects.get(id=course.teacher_id)])
    # courses = Course.objects.filter(id=usercourses.course_id)
    # courses=['C++', 'Java']
    return render_to_response('student_course.html', locals())


def student_group(request):
    links = [{'name': '学生页面', 'page': '/student/'}]
    list_num = 3
    user = User.objects.filter(name=request.session['name']).first()
    groups = ['534team', 'new course']
    return render_to_response('student_group.html', locals())


def student_course_i(request, i):
    links = [{'name': '学生页面', 'page': '/student/'}, {'name': '课程列表', 'page': '/student/course/'}]
    user = User.objects.filter(name=request.session['name']).first()
    course = Course.objects.get(id=i)
    term = Term.objects.filter(id=course.term_id).first()
    request.session['course_id'] = i
    teacher = User.objects.get(id=course.teacher_id)
    return render_to_response('student_course_i.html', locals())


def student_course_i_homework(request, i):
    user = User.objects.filter(name=request.session['name']).first()
    list_num = 1
    page_name = '作业列表'
    course = Course.objects.get(id=i)
    tasks = TaskRequirement.objects.filter(course_id=course.id)
    str1 = '/student/course/'
    str1 = str1 + str(course.id)
    links = [{'name': '学生页面', 'page': '/student/'},
             {'name': '课程列表', 'page': '/student/course/'}, {'name': course.name, 'page': str1}]
    return render_to_response('student_course_i_homework.html', locals())


def student_course_i_homework_I(request, i, I):
    list_num = 1
    page_name = '作业详情'
    course = Course.objects.get(id=i)
    teacher = User.objects.get(id=course.teacher_id)
    str1 = '/student/course/'
    str1 = str1 + str(course.id)
    links = [{'name': '学生页面', 'page': '/student/'},
             {'name': '课程列表', 'page': '/student/course/'}, {'name': course.name, 'page': str1}]

    user = User.objects.filter(name=request.session['name']).first()
    tasks = TaskFile.objects.filter(user_id=user.id, task_requirement_id=I)
    taskrequirement = TaskRequirement.objects.get(id=I)
    myurl = "/student/course/" + str(course.id)+"/homework/" + str(I)+"/"

    if request.method == "POST":
            task_file = TaskFile()
            task_file.name = taskrequirement.name
            task_file.is_file = False
            task_file.content = request.POST['content']
            task_file.group_id = 0
            task_file.task_requirement_id = taskrequirement.id
            task_file.user_id = user.id
            task_file.save()
            return HttpResponse(json.dumps(True))
    else:
        return render_to_response('student_course_i_homework_I.html', locals())



class UserForm(forms.Form):
    Description = forms.CharField(label='资源名称')
    File = forms.FileField(label='文件位置')


def student_course_i_homework_I_upload(request, i, I):
    list_num = 1
    page_name = '上传作业'
    course = Course.objects.get(id=i)
    str1 = '/student/course/'
    str1 = str1 + str(course.id)
    links = [{'name': '学生页面', 'page': '/student/'},
             {'name': '课程列表', 'page': '/student/course/'}, {'name': course.name, 'page': str1}]

    user = User.objects.filter(name=request.session['name']).first()
    tasks = TaskRequirement.objects.filter(course_id=course.id)
    teacher = User.objects.filter(id=course.teacher_id).first()
    term = Term.objects.filter(id=course.term_id).first()
    task = TaskRequirement.objects.get(pk=I)
    task_file = task.taskfile_set.all()

    if request.method == "POST":
        uf = UserForm(request.POST, request.FILES)
        if uf.is_valid():
            # 获取表单信息
            description = uf.cleaned_data['Description']
            filepath = uf.cleaned_data['File']
            # 写入数据库
            task_file = TaskFile()
            task_file.name = description
            task_file.server_path = filepath
            task_file.is_file = True
            task_file.group_id = 0
            task_file.task_requirement = task
            task_file.user = user
            task_file.save()

            course_id = int(request.session['course_id'])
            resources = Resource.objects.filter(course_id=course_id)
            return render_to_response('student_course_i_homework_I_upload.html', locals())
    else:
        uf = UserForm()

    return render_to_response('student_course_i_homework_I_upload.html', locals())


class UserForm_content(forms.Form):
    Description = forms.CharField(label='作业名字')
    Content = forms.CharField(label='作业内容',widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width:500px'}))

#
# def student_course_i_homework_I_content(request, i, I):
#     list_num = 1
#     page_name = '上传作业'
#     course = Course.objects.get(id=i)
#     str1 = '/student/course/'
#     str1 = str1 + str(course.id)
#     str2 = str1 + '/homework'
#     str3 = str2 + '/' + str(I)
#     links = [{'name': '学生页面', 'page': '/student/'},
#              {'name': '课程列表', 'page': '/student/course/'},
#              {'name': course.name, 'page': str1},
#              {'name': '作业列表', 'page': str2},
#              {'name': '作业信息', 'page': str3}]
#
#     user = User.objects.filter(name=request.session['name']).first()
#     tasks = TaskRequirement.objects.filter(course_id=course.id)
#     teacher = User.objects.filter(id=course.teacher_id).first()
#     term = Term.objects.filter(id=course.term_id).first()
#     task = TaskRequirement.objects.get(pk=I)
#     task_file = task.taskfile_set.all()
#
#     if request.method == "POST":
#         uf = UserForm_content(request.POST, request.FILES)
#         if uf.is_valid():
#             # 获取表单信息
#             description = uf.cleaned_data['Description']
#             content = uf.cleaned_data['Content']
#             # 写入数据库
#             task_file = TaskFile()
#             task_file.name = description
#             # task_file.server_path = filepath
#             task_file.is_file = False
#             task_file.content = content
#             task_file.group_id = 0
#             task_file.task_requirement = task
#             task_file.user = user
#             task_file.server_path = ''
#             task_file.save()
#
#             resources = Resource.objects.filter(course_id=i)
#             return render_to_response('student_course_i_homework_I_content.html', locals())
#     else:
#         uf = UserForm_content()
#
#     return render_to_response('student_course_i_homework_I_content.html', locals())


def student_course_i_resource(request, i):
    user = User.objects.filter(name=request.session['name']).first()
    list_num = 2
    page_name = '资源列表'
    course = Course.objects.get(id=i)
    resources = Resource.objects.filter(course_id=course.id)
    resourcesclasses = []
    for resource in resources:
        resourcesclasses.append([resource, ResourceClass.objects.get(id=resource.resource_class_id)])

    str1 = '/student/course/'
    str1 = str1 + str(course.id)
    links = [{'name': '学生页面', 'page': '/student/'},
             {'name': '课程列表', 'page': '/student/course/'}, {'name': course.name, 'page': str1}]
    return render_to_response('student_course_i_resource.html', locals())


def file_download(request, i, I):
    resource = Resource.objects.get(id=int(I))
    filename = resource.server_path
    f = open(str(filename))
    data = f.read()
    f.close()
    response = HttpResponse(data)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
