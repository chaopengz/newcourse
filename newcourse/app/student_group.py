# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import loader, context, RequestContext
import MySQLdb
from models import *
from django import forms


def addGroup(request):
    if request.method == 'POST':
        user = User.objects.filter(name=request.session['name']).first()
        name = request.POST['g_name']
        maxNum = request.POST['max']
        g = Group(name=name, max_number=maxNum, leader=user)
        g.save()
        return render_to_response('student_group.html')
    else:
        return render_to_response('student_add_group.html')


def myGroup(request):
    links = [{'name': '学生页面', 'page': '/student/'}]
    list_num = 3
    user = User.objects.filter(name=request.session['name']).first()

    g = Group.objects.filter()

    return render_to_response('student_group.html', locals())


def join(request):
    groupId = request.session['group_id']
    user = User.objects.filter(name=request.session['name']).first()
    uG = UserGroup(group_id=groupId, user=user)
    uG.save()
    return HttpResponse("加入成功")


def info(request, i):
    request.session['group_id'] = i
    return render_to_response('student_group_i.html', locals())
