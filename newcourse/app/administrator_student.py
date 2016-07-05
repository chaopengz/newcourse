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
     list_num=4
     page_name='学生管理'
     links=[ {'name': '学生管理', 'page': '/administrator/student/'} ]
     user=User.objects.filter(name=request.session['name']).first()
     students=User.objects.filter(type=2)
     return render_to_response('administrator_student.html', locals())

def reset_password(request,tId):
     student=User.objects.filter(type=2).get(id=tId)
     student.password='123'
     student.save()
     is_success='1'
     list_num=4
     page_name='学生管理'
     links=[{'name': '学生管理', 'page': '/administrator/student/'} ]
     user=User.objects.filter(name=request.session['name']).first()
     students=User.objects.filter(type=2)
     return render_to_response('administrator_student.html', locals())

def add_student(request):
    list_num = 4
    page_name = '添加学生'
    links=[{'name': '学生管理', 'page': '/administrator/student/'} , {'name': '添加学生', 'page': '/administrator/student/add_student'}]
    user=User.objects.get(name=request.session['name'])
    return render_to_response('administrator_add_student.html', locals())

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

def save_student(request):
    tname=request.POST['t_name']
    trealname=request.POST['t_realname']
    if request.POST.get('t_id'):
        student=User.objects.get(id=request.POST.get('t_id'))
        student.name=tname
        student.real_name=trealname
        student.save()
    else:
        student=User(
            name=tname,
            password='123',
            real_name=trealname,
            type=2
         )
        student.save()

    return HttpResponseRedirect('/administrator/student/')

