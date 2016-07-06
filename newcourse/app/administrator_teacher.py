# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb,json
from models import *
import datetime, calendar
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
    page_name = '添加教师'
    links=[{'name': '教师管理', 'page': '/administrator/teacher/'} , {'name': '添加教师', 'page': '/administrator/teacher/add_teacher'}]
    user=User.objects.get(name=request.session['name'])
    return render_to_response('administrator_add_teacher.html', locals())

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
            type=3,
            pic=''
         )
        teacher.save()

    return HttpResponseRedirect('/administrator/teacher/')

