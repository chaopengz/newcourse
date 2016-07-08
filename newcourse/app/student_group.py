# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import loader, context, RequestContext
import MySQLdb
from models import *
from django import forms


def addGroup(request):
    if request.method == 'POST':
        # Add group info to table app_group
        user = User.objects.filter(name=request.session['name']).first()
        name = request.POST['g_name']
        maxNum = request.POST['max']
        g = Group(name=name, max_number=maxNum, user=user)
        g.save()
        # Add group info to table app_userGroup
        groupId = g.id
        uG = UserGroup(group_id=groupId, user=user, is_allowed=1)
        uG.save()
        return render_to_response('student_mygroup.html')
    else:
        return render_to_response('student_add_group.html')


def myGroup(request):
    links = [{'name': '学生页面', 'page': '/student/'}]
    list_num = 3
    user = User.objects.filter(name=request.session['name']).first()

    uG = UserGroup.objects.filter(user=user)

    return render_to_response('student_mygroup.html', locals())


def join(request):
    groupId = request.session['group_id']
    user = User.objects.filter(name=request.session['name']).first()
    uG = UserGroup(group_id=groupId, user=user)
    uG.save()
    return HttpResponse("加入成功，待团队负责人审核")


def info(request, i):  # i stands for the groupId
    request.session['group_id'] = i
    user = User.objects.filter(name=request.session['name']).first()
    ug = UserGroup.objects.filter(user=user, group_id=i).filter()
    uG_len = len(ug)  # 用与判断用户是否存在userGroup中
    if uG_len > 0:
        is_allowed = ug.first().is_allowed
    return render_to_response('student_group_i.html', locals())
