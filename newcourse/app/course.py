# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *
import datetime, calendar


# Create your views here.

def main(request):
     list_num=2
     page_name='课程管理'
     links=[ {'name': '课程管理', 'page': '/course/'} ]
     user=User.objects.filter(name=request.session['name']).first()
     courses=Course.objects.all()
     res=[]
     for course in courses:
         isrun=compare_time(course.start_date, course.end_date)
         course.start_date=course.start_date.strftime("%Y年%m月%d日");
         course.end_date=course.end_date.strftime("%Y年%m月%d日");
         res.append(CourseShow(course,isrun))
     return render_to_response('administrator_course.html', locals())


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


def courseInfo(request, courseId):
     list_num = 2
     page_name = '课程详情'
     links=[{'name': '课程管理', 'page': '/course/'} , {'name': '课程详情', 'page': '/course/courseInfo'}]
     user=User.objects.filter(name=request.session['name']).first()
     course=Course.objects.filter(id=courseId).first()
     isrun=compare_time(course.start_date, course.end_date)
     course.start_date=course.start_date.strftime("%Y年%m月%d日")
     course.end_date=course.end_date.strftime("%Y年%m月%d日")
     res = CourseShow(course,isrun)
     return render_to_response('administrator_courseInfo.html', locals())

def course_task(request):
     list_num = 2
     page_name = '作业列表'
     links=[{'name': '作业管理', 'page': '/course/'} , {'name': '作业详情', 'page': '/course/task'}]
     user=User.objects.filter(name=request.session['name']).first()     teacher=User.objects.filter(id=course.teacher_id).first()
     term=Term.objects.filter(id=course.term_id).first()
     term.start_date=term.start_date.strftime("%Y年%m月%d日")
     term.end_date=term.end_date.strftime("%Y年%m月%d日")
     return render_to_response('courseInfo.html', locals())