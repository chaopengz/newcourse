# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *
import datetime, calendar


# Create your views here.

def main(request):
     links=[{'name': '首页', 'page': '/'}, {'name': '课程管理', 'page': '/student/'} ]
     user=User.objects.filter(name=request.session['name']).first()
     courses=Course.objects.all()
     res=[]
     for course in courses:

         isrun=compare_time(course.start_date, course.end_date)
         res.append(CourseShow(course,isrun))
     print type(courses[0].start_date)
     return render_to_response('administrator_course.html', locals())


class CourseShow:
    def __init__(self,course,isrun):
        self.course=course
        self.isrun=isrun

def compare_time(time1,time2):
    nowtime=datetime.date.today()
    print (time2-nowtime).days
    if (nowtime - time1).days > 0 and (time2-nowtime).days>0:
        return True
    else:
        return False