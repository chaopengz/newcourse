# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from models import *
from view_auth_manage import *


def t_Home(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '3'): return jump_no_auth(request)
    courseId = request.session['course_id']
    user = User.objects.filter(name=request.session['name']).first()
    c = Chat.objects.filter(courseid=courseId)
    user = User.objects.filter(name=request.session['name']).first()
    course_id = int(request.session['course_id'])
    course = Course.objects.get(id=course_id)
    links = [{'name': '课程管理', 'page': '/teacher/course'}, {'name': course.name, 'page': '/teacher/course'},
             {'name': '资源管理', 'page': '/teacher/course/resource'}]
    list_num = 4
    page_name = "课程交流"
    return render(request, "teacher_course_message.html", locals())


def s_Home(request, i):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    courseId = request.session['course_id']
    course = Course.objects.get(id=i)
    user = User.objects.filter(name=request.session['name']).first()
    list_num = 4
    page_name = "课程交流"
    c = Chat.objects.filter(courseid=courseId)
    str1 = '/student/course/'
    str1 = str1 + str(course.id)
    links = [{'name': '学生页面', 'page': '/student/'},
             {'name': '课程列表', 'page': '/student/course/'}, {'name': course.name, 'page': str1}]
    return render(request, "student_course_message.html", locals())


def Post(request):
    if not judge_login(request): return jump_not_login(request)
    if request.method == "POST":
        msg = request.POST['msgbox']
        user = User.objects.filter(name=request.session['name']).first()
        # if 'course_id' in request.session:
        courseId = request.session['course_id']
        c = Chat(user=user, message=msg, courseid=courseId)
        if msg != '':
            # print user, msg, courseId
            c.save()
        return JsonResponse({'msg': msg, 'user': c.user.real_name, 'pic': c.user.pic, 'time': c.created})
    else:
        return HttpResponse('Request must be POST.')


def Messages(request):
    if not judge_login(request): return jump_not_login(request)
    # courseId = 0
    # if 'course_id' in request.session:
    courseId = request.session['course_id']
    chat = Chat.objects.filter(courseid=courseId)
    loginUser = User.objects.filter(name=request.session['name']).first()

    return render(request, 'messages.html', locals())


def test(request):
    i = 1
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    courseId = request.session['course_id']
    course = Course.objects.get(id=i)
    loginUser = User.objects.filter(name=request.session['name']).first()
    list_num = 4
    page_name = "课程交流"
    chat = Chat.objects.filter(courseid=courseId)
    str1 = '/student/course/'
    str1 = str1 + str(course.id)
    links = [{'name': '学生页面', 'page': '/student/'},
             {'name': '课程列表', 'page': '/student/course/'}, {'name': course.name, 'page': str1}]
    # return render(request, "student_course_message.html", locals())
    return render(request, 'chat_test.html', locals())
