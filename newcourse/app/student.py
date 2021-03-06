# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import loader, context, RequestContext
import MySQLdb
from models import *
from django import forms
import json
import os, tempfile, zipfile,administrator_course
import datetime, calendar
from teacher_course import zip_dir
from view_auth_manage import *
# Create your views here.
class CourseShow:
    def __init__(self, course, isrun):
        self.course = course
        self.isrun = isrun

def student(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    links = [{'name': '学生页面', 'page': '/student/'}]
    if 'name' in request.session:
        name = request.session['name']
        user = User.objects.filter(name=name).first()
        if user is not None:
            return render_to_response('student.html', locals())
    return HttpResponseRedirect('/login/')


def student_info(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    links = [{'name': '学生页面', 'page': '/student/'}]
    list_num = 1
    user = User.objects.filter(name=request.session['name']).first()
    return render_to_response('student.html', locals())

# 比较课程的起止日期与系统当前日期，从而返回该课程是否已经结束
def compare_time(time1, time2):
    nowtime = datetime.date.today()
    print (time2 - nowtime).days
    if (nowtime - time1).days > 0 and (time2 - nowtime).days > 0:
        return True
    else:
        return False

def student_course(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    page_name = '课程列表'
    list_num = 2
    links = [{'name': '学生页面', 'page': '/student/'}]
    user = User.objects.filter(name=request.session['name']).first()

    usercourses = UserCourse.objects.filter(user_id=user.id)
    courses = []
    for usercourse in usercourses:
        course=Course.objects.get(id=usercourse.course_id)
        isrun=compare_time(course.start_date,course.end_date)
        courses.append(CourseShow(course, isrun))

    course_teachers = []
    for course in courses:
        course.course.start_date = course.course.start_date.strftime("%Y年%m月%d日")
        course.course.end_date = course.course.end_date.strftime("%Y年%m月%d日")
        course_teachers.append([course, User.objects.get(id=course.course.teacher_id)])
    sorted(course_teachers,)
    # courses = Course.objects.filter(id=usercourses.course_id)
    # courses=['C++', 'Java']
    return render_to_response('student_course.html', locals())


def student_course_i(request, i):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    user = User.objects.filter(name=request.session['name']).first()
    list_num = 1
    course = Course.objects.get(id=i)
    str1 = '/student/course/'
    str1 = str1 + str(course.id)
    links = [{'name': '学生页面', 'page': '/student/'},
             {'name': '课程列表', 'page': '/student/course/'}, {'name': course.name, 'page': str1}]
    course.start_date = course.start_date.strftime("%Y年%m月%d日")
    course.end_date = course.end_date.strftime("%Y年%m月%d日")
    term = Term.objects.filter(id=course.term_id).first()
    term.start_date = term.start_date.strftime("%Y年%m月%d日")
    term.end_date = term.end_date.strftime("%Y年%m月%d日")
    request.session['course_id'] = i
    teacher = User.objects.get(id=course.teacher_id)
    return render_to_response('student_course_i.html', locals())



def student_course_i_homework(request, i):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    user = User.objects.filter(name=request.session['name']).first()
    list_num = 2
    page_name = '作业列表'
    course = Course.objects.get(id=i)
    tasks = TaskRequirement.objects.filter(course_id=course.id)

    if course.is_single:
        task_dones =[]
        for task in tasks:
            task.start_date = task.start_date.strftime("%Y年%m月%d日")
            task.end_date = task.end_date.strftime("%Y年%m月%d日")
            task_dones.append([task,len(TaskFile.objects.filter(user_id=user.id,task_requirement_id=task.id))])
    else:

        groups1 = GroupCourse.objects.filter(course_id=i)
        groups2 = UserGroup.objects.filter(user_id=user.id, is_allowed=1)
        for group1 in groups1:
            for group2 in groups2:
                if group1.group_id == group2.group_id:
                    group_id = group1.group_id
        task_dones = []
        for task in tasks:
            task.start_date = task.start_date.strftime("%Y年%m月%d日")
            task.end_date = task.end_date.strftime("%Y年%m月%d日")
            task_dones.append([task, len(TaskFile.objects.filter(group_id=group_id, task_requirement_id=task.id))])
    str1 = '/student/course/'
    str1 = str1 + str(course.id)
    links = [{'name': '学生页面', 'page': '/student/'},
             {'name': '课程列表', 'page': '/student/course/'}, {'name': course.name, 'page': str1}]
    return render_to_response('student_course_i_homework.html', locals())

def student_course_homework_task_delete(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    taskfile=TaskFile.objects.get(pk=request.POST['taskfileid'])
    taskfile.delete()
    return HttpResponse(json.dumps(True))

def student_course_i_homework_I(request, i, I):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    list_num = 2
    page_name = '作业详情'
    course = Course.objects.get(id=i)
    teacher = User.objects.get(id=course.teacher_id)
    str1 = '/student/course/'
    str1 = str1 + str(course.id)
    str2 = str1 + '/homework/'
    links = [{'name': '学生页面', 'page': '/student/'},
             {'name': '课程列表', 'page': '/student/course/'}, {'name': course.name, 'page': str1},{'name': '作业列表', 'page': str2}]
    uf = UserForm(request.POST, request.FILES)
    user = User.objects.filter(name=request.session['name']).first()
    tasks = TaskFile.objects.filter(user_id=user.id, task_requirement_id=I)
    allow_upload = 1
    group_id = 0
    if course.is_single ==0:
        groups1 = GroupCourse.objects.filter(course_id=i)
        groups2 = UserGroup.objects.filter(user_id = user.id,is_allowed=1)
        for group1 in groups1:
            for group2 in groups2:
                if group1.group_id ==group2.group_id:
                    group_id=  group1.group_id
                    group = Group.objects.get(id = group_id)
                    tasks = TaskFile.objects.filter(group_id=group_id,task_requirement_id=I)
                    if len(tasks)!=0:
                        allow_upload =0
                        if group.user_id==user.id:
                            allow_upload =1
    taskrequirement = TaskRequirement.objects.get(id=I)
    myurl = "/student/course/" + str(course.id)+"/homework/" + str(I)+"/"
    if not administrator_course.compare_time(taskrequirement.start_date, taskrequirement.end_date):
        allow_upload = 0
    if request.method == "POST":
        uf = UserForm(request.POST, request.FILES)

        if not uf.is_valid():
            request.session['message'] = "作业描述或文件为空"
            request.session['nexturl'] = str1+'/homework/'+ str(I)
            return HttpResponseRedirect('/info/')


        '''description = uf.cleaned_data['Description']
        filepath = uf.cleaned_data['File']
        if not description:
            request.session['message'] = "作业描述为空"
            request.session['nexturl'] = str1
            return HttpResponseRedirect('/info/')

        if not filepath:
            request.session['message'] = "未选择文件"
            request.session['nexturl'] = str1
            return HttpResponseRedirect('/info/')'''

        if not administrator_course.compare_time(taskrequirement.start_date, taskrequirement.end_date):
            request.session['message'] = "本次作业已过期"
            request.session['nexturl'] = str1
            return HttpResponseRedirect('/info/')


        if uf.is_valid():
            # 获取表单信息
            description = uf.cleaned_data['Description']
            filepath = uf.cleaned_data['File']
            # 写入数据库】
            task_file = TaskFile.objects.filter(task_requirement_id=taskrequirement.id, user=user)
            if task_file:
                task_file[0].delete()
            task_file = TaskFile()
            task_file.name = description
            task_file.server_path = filepath
            task_file.is_file = True
            task_file.group_id = group_id
            task_file.task_requirement_id = taskrequirement.id
            task_file.user = user
            task_file.save()

            course_id = int(request.session['course_id'])
            resources = Resource.objects.filter(course_id=course_id)
            return HttpResponseRedirect('/student/course/' + i + '/homework/' + I + '/')
    else:
        uf = UserForm()
    if request.method == "POST":
            if not administrator_course.compare_time(taskrequirement.start_date, taskrequirement.end_date):
                 request.session['message'] = "本次作业已过期"
                 request.session['nexturl'] = myurl
                 return HttpResponseRedirect('/info/')
            task_file = TaskFile.objects.filter(task_requirement_id=taskrequirement.id, user=user)
            if task_file:
                task_file[0].delete()
            task_file = TaskFile()
            task_file.name = taskrequirement.name
            task_file.is_file = False
            task_file.content = request.POST['content']
            task_file.group_id = group_id
            task_file.task_requirement_id = taskrequirement.id
            task_file.user_id = user.id
            task_file.server_path = ''
            task_file.save()
            return HttpResponse(json.dumps(True))
    else:
        taskrequirement.start_date = taskrequirement.start_date.strftime("%Y年%m月%d日")
        taskrequirement.end_date = taskrequirement.end_date.strftime("%Y年%m月%d日")
        for task in tasks:
            task.submit_time = task.submit_time.strftime("%Y年%m月%d日%H时%M分")
        return render_to_response('student_course_i_homework_I.html', locals())


def student_course_i_homework_I_submit(request, i, I):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    list_num = 1
    page_name = '作业详情'
    course = Course.objects.get(id=i)
    teacher = User.objects.get(id=course.teacher_id)
    str1 = '/student/course/'
    str1 = str1 + str(course.id)
    links = [{'name': '学生页面', 'page': '/student/'},
             {'name': '课程列表', 'page': '/student/course/'}, {'name': course.name, 'page': str1}]
    uf = UserForm(request.POST, request.FILES)
    user = User.objects.filter(name=request.session['name']).first()
    tasks = TaskFile.objects.filter(user_id=user.id, task_requirement_id=I)
    for task in tasks:
        task.submit_time = task.submit_time.strftime("%Y年%m月%d日")
    allow_upload = 1
    group_id = 0
    if course.is_single == 0:
        groups1 = GroupCourse.objects.filter(course_id=i)
        groups2 = UserGroup.objects.filter(user_id=user.id, is_allowed=1)
        for group1 in groups1:
            for group2 in groups2:
                if group1.group_id == group2.group_id:
                    group_id = group1.group_id
                    group = Group.objects.get(id=group_id)
                    tasks = TaskFile.objects.filter(group_id=group_id, task_requirement_id=I)
                    if len(tasks) != 0:
                        allow_upload = 0
                        if group.user_id == user.id:
                            allow_upload = 1
    taskrequirement = TaskRequirement.objects.get(id=I)
    myurl = "/student/course/" + str(course.id) + "/homework/" + str(I) + "/"
    if not administrator_course.compare_time(taskrequirement.start_date, taskrequirement.end_date):
        allow_upload = 0
    if request.method == "POST":
        if not administrator_course.compare_time(taskrequirement.start_date, taskrequirement.end_date):
            request.session['message'] = "本次作业已过期"
            request.session['nexturl'] = myurl
            return HttpResponseRedirect('/info/')
        task_file = TaskFile.objects.filter(task_requirement_id=taskrequirement.id, user=user)
        if task_file:
            task_file[0].delete()
        task_file = TaskFile()
        task_file.name = taskrequirement.name
        task_file.is_file = False
        task_file.content = request.POST['content']
        task_file.group_id = group_id
        task_file.task_requirement_id = taskrequirement.id
        task_file.user_id = user.id
        task_file.server_path = ''
        task_file.save()
        return HttpResponse(json.dumps(True))
    else:
        taskrequirement.start_date = taskrequirement.start_date.strftime("%Y年%m月%d日")
        taskrequirement.end_date = taskrequirement.end_date.strftime("%Y年%m月%d日")
        return render_to_response('student_course_i_homework_I.html', locals())









class UserForm(forms.Form):
    Description = forms.CharField(label='资源名称')
    File = forms.FileField(label='文件位置')


def student_course_i_homework_I_upload(request, i, I):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
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
    str1 = str1 + str('/homework/') + str(task.id)
    task_file = task.taskfile_set.all()
    group_id = 0
    if course.is_single == 0:
        groups1 = GroupCourse.objects.filter(course_id=i)
        groups2 = UserGroup.objects.filter(user_id=user.id, is_allowed=1)
        for group1 in groups1:
            for group2 in groups2:
                if group1.group_id == group2.group_id:
                    group_id = group1.group_id
    if request.method == "POST":
        if  not administrator_course.compare_time(task.start_date,task.end_date):
            request.session['message'] = "本次作业已过期"
            request.session['nexturl'] = str1
            return HttpResponseRedirect('/info/')

        uf = UserForm(request.POST, request.FILES)
        if uf.is_valid():
            # 获取表单信息
            description = uf.cleaned_data['Description']
            filepath = uf.cleaned_data['File']
            # 写入数据库】
            task_file = TaskFile.objects.get(task_requirement = task,user = user)
            task_file.delete()
            task_file = TaskFile()
            task_file.name = description
            task_file.server_path = filepath
            task_file.is_file = True
            task_file.group_id = group_id
            task_file.task_requirement = task
            task_file.user = user
            task_file.save()

            course_id = int(request.session['course_id'])
            resources = Resource.objects.filter(course_id=course_id)
            return HttpResponseRedirect('/student/course/' + i + '/homework/' + I + '/')
    else:
        uf = UserForm()

    return render_to_response('student_course_i_homework_I_upload.html', locals())


class UserForm_content(forms.Form):
    Description = forms.CharField(label='作业名字')
    Content = forms.CharField(label='作业内容',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width:500px'}))

def student_course_i_resource(request, i):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    user = User.objects.filter(name=request.session['name']).first()
    list_num = 3
    page_name = '资源列表'
    course = Course.objects.get(id=i)
    resources = Resource.objects.filter(course_id=course.id)
    resourcesclasses = []
    for resource in resources:
        resource.submit_time = resource.submit_time.strftime("%Y年%m月%d日%H时%M分")
        resourcesclasses.append([resource, ResourceClass.objects.get(id=resource.resource_class_id)])
    str1 = '/student/course/'
    str1 = str1 + str(course.id)
    links = [{'name': '学生页面', 'page': '/student/'},
             {'name': '课程列表', 'page': '/student/course/'}, {'name': course.name, 'page': str1}]
    return render_to_response('student_course_i_resource.html', locals())


def file_download(request, i, I):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    resource = Resource.objects.get(id=int(I))
    filename = resource.server_path
    f = open(str(filename))
    data = f.read()
    f.close()
    response = HttpResponse(data)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def one_click_download(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    user = User.objects.filter(name=request.session['name']).first()
    course_id = request.session['course_id']
    dir = '/media/resource/' + course_id
    file = '/media/temp.zip'
    root_dir = os.path.dirname(__file__)
    zip_dir(root_dir[:-4] + dir, root_dir[:-4] + file)
    return HttpResponseRedirect(file)


def student_group(request):
    page_name = '所有团队'
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    links = [{'name': '学生页面', 'page': '/student/'}]
    list_num = 4
    user = User.objects.filter(name=request.session['name']).first()
    g = Group.objects.filter()
    request.session['list_num'] = 4

    return render_to_response('student_allgroups.html', locals())
