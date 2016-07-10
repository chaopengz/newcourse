# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb,json
from models import *
import datetime, calendar
import os
import random
import csv
import time
from view_auth_manage import *
# Create your views here.

def main(request):
     if not judge_login(request): return jump_not_login(request)
     if not judge_auth(request, '1'): return jump_no_auth(request)
     is_success='0'
     list_num=4
     page_name='学生管理'
     links=[ {'name': '学生管理', 'page': '/administrator/student/'} ]
     user=User.objects.filter(name=request.session['name']).first()
     students=User.objects.filter(type=2)
     return render_to_response('administrator_student.html', locals())

def reset_password(request,tId):
     if not judge_login(request): return jump_not_login(request)
     if not judge_auth(request, '1'): return jump_no_auth(request)
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
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    list_num = 4
    page_name = '添加学生'
    links=[{'name': '学生管理', 'page': '/administrator/student/'} , {'name': '添加学生', 'page': '/administrator/student/add_student'}]
    user=User.objects.get(name=request.session['name'])
    return render_to_response('administrator_add_student.html', locals())

def add_student_many(request):
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
                    if User.objects.filter(name=row[0].decode('gb2312'),type=2).count() == 0:
                        new_student=User(
                            name=row[0].decode('gb2312'),
                            password='123',
                            real_name=row[1].decode('gb2312'),
                            type=2,
                            pic=''
                        )
                        new_student.save()
                rownum+=1
        os.remove(fullpath)
        request.session['message'] = "学生信息导入成功"
        request.session['nexturl'] = "/administrator/student/"
        return HttpResponseRedirect('/info/')
    else:
        return HttpResponseRedirect('/administrator/student/')

def save_student(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
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
            type=2,
            pic=''
         )
        student.save()

    return HttpResponseRedirect('/administrator/student/')

