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
     is_success='0'
     list_num=3
     page_name='教师管理'
     links=[ {'name': '教师管理', 'page': '/administrator/teacher/'} ]
     user=User.objects.filter(name=request.session['name']).first()
     teachers=User.objects.filter(type=3)
     return render_to_response('administrator_teacher.html', locals())

def reset_password(request,tId):
     teacher=User.objects.filter(type=3).get(id=tId)
     teacher.password='123'
     teacher.save()
     is_success='1'
     list_num=3
     page_name='教师管理'
     links=[ {'name': '教师管理', 'page': '/administrator/teacher/'} ]
     user=User.objects.filter(name=request.session['name']).first()
     teachers=User.objects.filter(type=3)
     return render_to_response('administrator_teacher.html', locals())

def add_teacher(request):
    list_num = 2
    page_name = '添加课程'
    links=[{'name': '教师管理', 'page': '/administrator/teacher/'} , {'name': '添加教师', 'page': '/administrator/teacher/add_teacher'}]
    user=User.objects.get(name=request.session['name'])
    return render_to_response('administrator_add_teacher.html', locals())

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

def save_teacher(request):
    tname=request.POST['t_name']
    trealname=request.POST['t_realname']
    if request.POST.get('t_id'):
        teacher=User.objects.get(id=request.POST.get('t_id'))
        teacher.name=tname
        teacher.real_name=trealname
        teacher.save()
    else:
        teacher=User(
            name=tname,
            password='123',
            real_name=trealname,
            type=3
         )
        teacher.save()

    return HttpResponseRedirect('/administrator/teacher/')

