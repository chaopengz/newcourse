# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb,json
from models import *
import datetime, calendar
from django import forms
# Create your views here.

def main(request):
     list_num=2
     page_name='课程管理'
     links=[ {'name': '课程管理', 'page': '/administrator/course/'} ]
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
     links=[{'name': '课程管理', 'page': '/administrator/course/'} , {'name': '课程详情', 'page': '/administrator/course/courseInfo/'+courseId}]
     user=User.objects.filter(name=request.session['name']).first()
     course=Course.objects.filter(id=courseId).first()
     isrun=compare_time(course.start_date, course.end_date)
     course.start_date=course.start_date.strftime("%Y年%m月%d日")
     course.end_date=course.end_date.strftime("%Y年%m月%d日")
     res = CourseShow(course,isrun)
     teacher=User.objects.filter(id=course.teacher_id).first()
     term=Term.objects.filter(id=course.term_id).first()
     term.start_date=term.start_date.strftime("%Y年%m月%d日")
     term.end_date=term.end_date.strftime("%Y年%m月%d日")
     return render_to_response('administrator_courseInfo.html', locals())

def addCourseShow(request):
    list_num = 2
    page_name = '添加课程'
    links=[{'name': '课程管理', 'page': '/administrator/course/'} , {'name': '添加课程', 'page': '/administrator/course/add_course'}]
    user=User.objects.get(name=request.session['name'])
    #下拉列表的东西
    teachers=User.objects.filter(type=3)
    terms=Term.objects.all()
    # terms=Term.objects.filter(start_date__lte=datetime.date.today()).filter(end_date__gte=datetime.date.today())

    return render_to_response('administrator_add_course.html', locals())

def changeCourseShow(request,courseId):
    list_num = 2
    page_name = '添加课程'
    links=[{'name': '课程管理', 'page': '/administrator/course/'} , {'name': '添加课程', 'page': '/administrator/course/change_course/'+courseId}]
    user=User.objects.get(name=request.session['name'])

    course=Course.objects.get(id=courseId)
    #更改日期格式便于显示在日期框里
    course.start_date=course.start_date.strftime("%m/%d/%Y")
    course.end_date=course.end_date.strftime("%m/%d/%Y")
    #课程所对应信息
    teacher=User.objects.get(id=course.teacher_id)
    term=Term.objects.get(id=course.term_id)
    #下拉列表的东西
    teachers=User.objects.filter(type=3)
    terms=Term.objects.all()
    # terms=Term.objects.filter(start_date__lte=datetime.date.today()).filter(end_date__gte=datetime.date.today())
    return render_to_response('administrator_change_course.html', locals())

def save_course(request):
    list_num = 2
    page_name = '课程详情'
    links=[{'name': '课程管理', 'page': '/administrator/course/'} , {'name': '课程详情', 'page': '/administrator/course/courseInfo/'}]
    user=User.objects.filter(name=request.session['name']).first()

    tname=request.POST['t_name']
    tintroduction=request.POST['t_introduction']
    tteacher=request.POST['t_teacher']
    tterm=request.POST['t_term']
    if request.POST['t_is_single'] == 2:
        tis_single=0
    else:
        tis_single=1
    tdate=request.POST['t_date']
    sdatestr=tdate[0:10]
    edatestr=tdate[13:23]
    sdate=datetime.datetime.strptime(sdatestr, "%m/%d/%Y").date()
    edate=datetime.datetime.strptime(edatestr, "%m/%d/%Y").date()

    if request.POST.get('t_id'):
        course=Course.objects.get(id=request.POST.get('t_id'))
        course.name=tname
        course.introduction=tintroduction
        course.teacher_id=tteacher
        course.term_id=tterm
        course.is_single=tis_single
        course.start_date=sdate
        course.end_date=edate
        course.save()
    else:
        course=Course(
            name=tname,
            introduction=tintroduction,
            teacher_id=tteacher,
            term_id=tterm,
            is_single=tis_single,
            start_date=sdate,
            end_date=edate
         )
        course.save()

    return HttpResponseRedirect('/administrator/course/courseInfo/'+str(course.id))

