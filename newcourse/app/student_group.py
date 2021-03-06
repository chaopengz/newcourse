# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import loader, context, RequestContext
import MySQLdb
from models import *
from django import forms
from view_auth_manage import *

def addGroup(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    user = User.objects.filter(name=request.session['name']).first()
    list_num = request.session['list_num']
    links = [{'name': '学生页面', 'page': '/student/'},{ 'name': '所有团队', 'page': '/student/groups/'}]
    if list_num ==3:
        links = [{'name': '学生页面', 'page': '/student/'},{'name':'我的团队','page':'/student/mygroup/'}]
    if request.method == 'POST':
        # Add group info to table app_group
        user = User.objects.filter(name=request.session['name']).first()
        name = request.POST['g_name']
        maxNum = request.POST['max']
        if int(maxNum)<=0:
            return jump_with_info(request,"团队最大人数填写有误，请修改。","/student/mygroup/")
        else:
            g = Group(name=name, max_number=maxNum, user=user)
            g.save()
            # Add group info to table app_userGroup
            groupId = g.id
            uG = UserGroup(group_id=groupId, user=user, is_allowed=1)
            uG.save()
            return HttpResponseRedirect('/student/mygroup/')
    else:
        return render_to_response('student_add_group.html',locals())


def myGroup(request):
    page_name = '我的团队'
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    links = [{'name': '学生页面', 'page': '/student/'}]
    list_num = 3
    user = User.objects.filter(name=request.session['name']).first()
    request.session['list_num'] = 3
    uG = UserGroup.objects.filter(user=user)

    return render_to_response('student_mygroup.html', locals())


def join(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    groupId = request.session['group_id']
    user = User.objects.filter(name=request.session['name']).first()
    uG = UserGroup(group_id=groupId, user=user)
    uG.save()
    print 'success'
    return HttpResponse("申请加入成功，待团队负责人审核")


def info(request, i):  # i stands for the groupId
    page_name = "团队详情"
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    request.session['group_id'] = i
    list_num = request.session['list_num']
    links = [{'name': '学生页面', 'page': '/student/'},{ 'name': '所有团队', 'page': '/student/groups/'}]
    if list_num == 3:
        links = [{'name': '学生页面', 'page': '/student/'},{ 'name': '我的团队', 'page': '/student/mygroup/'}]
    user = User.objects.filter(name=request.session['name']).first()
    ug = UserGroup.objects.filter(user=user, group_id=i)
    group = Group.objects.filter(id=i).first()  # 组的信息
    group_courses = GroupCourse.objects.filter(group_id=i,is_allowed='1') #the courses which the group took

    apply_course_len = len(GroupCourse.objects.filter(group_id=i))

    courses=[]
    for group_course in group_courses:
        courses.append(Course.objects.get(id=group_course.course_id))
    course_teachers=[]
    for course in courses:
        course.start_date = course.start_date.strftime("%Y年%m月%d日")
        course.end_date = course.end_date.strftime("%Y年%m月%d日")
        course_teachers.append([course, User.objects.get(id=course.teacher_id)])
    sorted(course_teachers,)
    course_teachers_len=len(course_teachers)

    group_user = User.objects.filter(id=group.user_id).first()#负责人
    group_member=UserGroup.objects.filter(group_id=i)
    member_list=[]
    no_member_list=[]
    for member in group_member:
        if member.user_id !=group_user.id:
            if member.is_allowed ==1:
                member_list.append(User.objects.get(id=member.user_id))
            elif member.is_allowed==0:
                if group.end == 1:#如果开启了组队请求
                    no_member_list.append(User.objects.get(id=member.user_id))
                else:#如果关闭了组队请求
                    member.is_allowed=2
    no_member_list_len=len(no_member_list)
    uG_len = len(ug)  # 用与判断用户是否存在userGroup中
    if uG_len > 0:
        is_allowed = ug.first().is_allowed
    if group_user.id != user.id:#r如果是负责人
        return render_to_response('student_group_info.html', locals())
    else:#如果不是负责人
        return render_to_response('student_group_info_owner.html',locals())

def handle_application(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    ug = UserGroup.objects.filter(user_id=request.POST['user_id'], group_id=request.POST['group_id']).first()
    ug.is_allowed = request.POST['is_allowed']
    if ug.is_allowed == "1":
        group = Group.objects.filter(id=request.POST['group_id']).first()
        if group.number ==group.max_number:
            ug.is_allowed = 2
            ug.save()
            return HttpResponse("2")
        group.number += 1

        if group.number == group.max_number:
            group.end = 0
        group.save()
        ug.save()
        return HttpResponse("1")
    else:
        ug.save()
        return HttpResponse("2")

def authority_translate(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    group=Group.objects.get(id=request.POST['group_id'])
    group.user_id=request.POST['user_id']
    group.save()
    return HttpResponse("权限转让成功")

def handle_group(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    if request.method == 'POST':
        gid = request.POST['group_id']
        handle_type = request.POST['type']
        if handle_type == "1":
            group = Group.objects.filter(id=gid).first()
            if(group.end==1):
                group.end = 0
                group.save()
                return HttpResponse("成功关闭组队申请！")
            '''else:
                group.end = 1
                group.save()
                return HttpResponse("成功开启组队申请！")'''
        else:
            UserGroup.objects.filter(group_id=gid).delete()
            GroupCourse.objects.filter(group_id=gid).delete()
            Group.objects.get(id=gid).delete()
            return HttpResponse("成功解散团队!")

def applyforcourse(request):
    page_name = "课程列表"
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    user = User.objects.filter(name=request.session['name']).first()
    list_num = request.session['list_num']
    group = Group.objects.get(id = request.session['group_id'])
    links = [{'name': '学生页面', 'page': '/student/'}, {'name': '所有团队', 'page': '/student/groups/'}, {'name': '当前团队', 'page': '/student/group/groupInfo/'+str(group.id)}]
    if list_num == 3:
        links = [{'name': '学生页面', 'page': '/student/'}, {'name': '我的团队', 'page': '/student/mygroup/'},{'name': '当前团队', 'page': '/student/group/groupInfo/'+str(group.id)+'/'}]
    #courses2 = Course.objects.filter(is_single = 0)
    #courses = []
    #for course in courses2:
     #   if not GroupCourse.objects.filter(group_id = request.session['group_id'],course_id=course.id):
     #       courses.append(course)
    course_teachers = []
    courses = Course.objects.filter(is_single=0)
    for course in courses:
        course.start_date = course.start_date.strftime("%Y年%m月%d日")
        course.end_date = course.end_date.strftime("%Y年%m月%d日")
        course_teachers.append([course, User.objects.get(id=course.teacher_id)])
    return render_to_response('student_group_applyforcourse.html',locals())


def applyforcourse_i(request,i):
    page_name = '选课'
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    list_num = request.session['list_num']
    group = Group.objects.get(id=request.session['group_id'])
    links = [{'name': '学生页面', 'page': '/student/'}, {'name': '所有团队', 'page': '/student/groups/'},{'name': '当前团队', 'page': '/student/group/groupInfo/'+str(group.id)},{'name':'课程列表','page':'/student/group/applyforcourse/'}]
    if list_num == 3:
        links = [{'name': '学生页面', 'page': '/student/'}, {'name': '我的团队', 'page': '/student/mygroup/'},{'name': '当前团队', 'page': '/student/group/groupInfo/'+str(group.id)},{'name':'课程列表','page':'/student/group/applyforcourse/'}]
    user = User.objects.filter(name=request.session['name']).first()
    request.session['course_id'] = i
    course = Course.objects.get(id = i)
    teacher = User.objects.get(id = course.teacher_id)
    term = Term.objects.get(id = course.term_id)
    group = Group.objects.get(id = request.session["group_id"])
    groupcourse = GroupCourse.objects.filter(group_id=group.id,course_id=course.id)
    course.start_date = course.start_date.strftime("%Y年%m月%d日")
    course.end_date = course.end_date.strftime("%Y年%m月%d日")
    term.start_date = term.start_date.strftime("%Y年%m月%d日")
    term.end_date = term.end_date.strftime("%Y年%m月%d日")
    return render_to_response('student_group_applyforcourse_i.html', locals())

def apply(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '2'): return jump_no_auth(request)
    user = User.objects.filter(name=request.session['name']).first()
    course = Course.objects.get(id = request.session['course_id'])
    teacher = User.objects.get(id = course.teacher_id)
    term = Term.objects.get(id = course.term_id)
    group = Group.objects.get(id = request.session["group_id"])
    usercourses = UserCourse.objects.filter(course_id = course.id)
    usergroups = UserGroup.objects.filter(group_id=group.id,is_allowed=1)
    valid = 1
    for usercourse in usercourses:
        for usergroup in usergroups:
            if usercourse.user_id==usergroup.user_id:
                valid = 0
                       #somebody in the group had been in the course
    groupcourse = GroupCourse.objects.filter(group_id=group.id,course_id = course.id)
    aplied = 0
    if groupcourse:
        applied = 1
    applied_user = User.objects.filter()
    if group.user_id ==user.id:
        if course.is_single == 0:
            if valid == 1:
                if aplied ==0:
                    groupcourse = GroupCourse()
                    #test
                    groupcourse.is_allowed = 0
                    groupcourse.course_id = course.id
                    groupcourse.group_id = group.id
                    groupcourse.save()
                    request.session['message'] = "申请成功\n"
                    request.session['nexturl'] = "/student/group/applyforcourse/"
                    return HttpResponseRedirect('/info/')
                request.session['message'] = "你的团队中已经申请了这门课程\n"
                request.session['nexturl'] = "/student/group/applyforcourse/"
                return HttpResponseRedirect('/info/')
            request.session['message'] = "你的团队中已经有人加入了这门课程\n"
            request.session['nexturl'] = "/student/group/applyforcourse/"
            return HttpResponseRedirect('/info/')
        request.session['message'] = "这门课不可以团队选课\n"
        request.session['nexturl'] = "/student/group/applyforcourse/"
        return HttpResponseRedirect('/info/')
    request.session['message'] = "你不是这个团队的负责人\n"
    request.session['nexturl'] = "/student/group/applyforcourse/"
    return HttpResponseRedirect('/info/')
