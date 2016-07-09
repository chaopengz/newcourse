# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *
from view_auth_manage import *

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
     courses = Course.objects.filter(teacher_id=user.id)
     return render_to_response('teacher_course_info.html', locals())
