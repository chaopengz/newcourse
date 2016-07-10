# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb,json
from models import *
import datetime, calendar
import os
import time
import random
import csv
from view_auth_manage import *
# Create your views here.

def main(request):
     if not judge_login(request): return jump_not_login(request)
     if not judge_auth(request, '1'): return jump_no_auth(request)
     is_success='0'
     list_num=3
     page_name='教师管理'
     links=[ {'name': '教师管理', 'page': '/administrator/teacher/'} ]
     user=User.objects.filter(name=request.session['name']).first()
     teachers=User.objects.filter(type=3)
     return render_to_response('administrator_teacher.html', locals())

def reset_password(request,tId):
     if not judge_login(request): return jump_not_login(request)
     if not judge_auth(request, '1'): return jump_no_auth(request)
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
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    list_num = 3
    page_name = '添加教师'
    links=[{'name': '教师管理', 'page': '/administrator/teacher/'} , {'name': '添加教师', 'page': '/administrator/teacher/add_teacher'}]
    user=User.objects.get(name=request.session['name'])
    return render_to_response('administrator_add_teacher.html', locals())



def add_teacher_many(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    if 'infolist' in request.FILES:
        file = request.FILES.get('infolist', None)
        filedata=file.read()
        basename=str(time.time()).replace('.','_')+str(random.randrange(0,99999,1))


        path='%s/uploads/' % (os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media'))
        # 如果文件夹不存在，创建文件夹
        if not os.path.exists(path):
            os.makedirs(path)
        fullpath=path+basename
        f = open(fullpath, 'wb')
        f.write(filedata)
        f.close()
        with open(fullpath,'rb') as f:
            reader = csv.reader(f)
            rownum=0
            for row in reader:
                if rownum>0:
                    if User.objects.filter(name=row[0].decode('gb2312'),type=3).count() == 0:
                        new_student=User(
                            name=row[0].decode('gb2312'),
                            password='123',
                            real_name=row[1].decode('gb2312'),
                            type=3,
                            pic=''
                        )
                        new_student.save()
                rownum+=1
        os.remove(fullpath)
        request.session['message'] = "教师信息导入成功"
        request.session['nexturl'] = "/administrator/teacher/"
        return HttpResponseRedirect('/info/')
    else:
        return HttpResponseRedirect('/administrator/teacher/')


def save_teacher(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
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

