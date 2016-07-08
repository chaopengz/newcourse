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
    print 'success'
    return HttpResponse("申请加入成功，待团队负责人审核")


def info(request, i):  # i stands for the groupId
    request.session['group_id'] = i
    user = User.objects.filter(name=request.session['name']).first()
    ug = UserGroup.objects.filter(user=user, group_id=i)
    group = Group.objects.filter(id=i).first()  # 组的信息
    group_user = User.objects.filter(id=group.user_id).first()  # 负责人
    group_member = UserGroup.objects.filter(group_id=i)
    member_list = []
    no_member_list = []
    for member in group_member:
        if member.user_id != group_user.id:
            if member.is_allowed == 1:
                member_list.append(User.objects.get(id=member.user_id))
            else:
                no_member_list.append(User.objects.get(id=member.user_id))
    no_member_list_len = len(no_member_list)
    uG_len = len(ug)  # 用与判断用户是否存在userGroup中
    if uG_len > 0:
        is_allowed = ug.first().is_allowed
    if group_user.id != user.id:  # r如果是负责人
        return render_to_response('student_group_info.html', locals())
    else:  # 如果不是负责人
        return render_to_response('student_group_info_owner.html', locals())


def handle_application(request):
    ug = UserGroup.objects.filter(user_id=request.POST['user_id'], group_id=request.POST['group_id']).first()
    ug.is_allowed = request.POST['is_allowed']
    if ug.is_allowed == "1":
        group = Group.objects.filter(id=request.POST['group_id']).first()
        group.number += 1
        group.save()
        return HttpResponse("1")
    else:
        ug.save()
        return HttpResponse("2")


def handle_group(request):
    return HttpResponse("处理团队申请")
