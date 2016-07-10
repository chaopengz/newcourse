# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *
from view_auth_manage import *

# 比较课程的起止日期与系统当前日期，从而返回该课程是否已经结束
def compare_time(time1, time2):
    nowtime = datetime.date.today()
    print (time2 - nowtime).days
    if (nowtime - time1).days > 0 and (time2 - nowtime).days > 0:
        return True
    else:
        return False

# Create your views here.
def teacher_info(request):
     if not judge_login(request): return jump_not_login(request)
     if not judge_auth(request, '3'): return jump_no_auth(request)
     links=[{'name': '教师页面', 'page': '/teacher/'} ]
     list_num = 1
     page_name = '作业列表'
     if 'name' in request.session:
          name = request.session['name']
          user=User.objects.filter(name=name).first()
          if user is not None:
               return render_to_response('teacher_info.html', locals())
     return HttpResponseRedirect('/login/')


def teacher_course(request):
     if not judge_login(request): return jump_not_login(request)
     if not judge_auth(request, '3'): return jump_no_auth(request)
     list_num = 2
     page_name = '作业列表'
     links = [{'name': '教师页面', 'page': '/teacher/'}]
     user = User.objects.filter(name=request.session['name']).first()
     courses = Course.objects.filter(teacher_id=user.id).order_by('-end_date')
     res=[]

     for course in courses:
           isrun = compare_time(course.start_date, course.end_date)
           course.start_date = course.start_date.strftime("%Y年%m月%d日")
           course.end_date = course.end_date.strftime("%Y年%m月%d日")
           res.append(CourseShow(course,isrun))

     return render_to_response('teacher_course_info.html', locals())

class CourseShow:
    def __init__(self, course, isrun):
        self.course = course
        self.isrun = isrun

