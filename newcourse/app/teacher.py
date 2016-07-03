# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *


# Create your views here.

def teacher(request):
     links=[{'name': '首页', 'page': '/'}, {'name': '教师页面', 'page': '/teacher/'} ]
     if 'name' in request.session:
          name = request.session['name']
          user=User.objects.filter(name=name).first()
          if user is not None:
               return render_to_response('teacher.html', locals())
     return HttpResponseRedirect('/login/')


def teacher_info(request):
     links = [{'name': '首页', 'page': '/'}, {'name': '教师页面', 'page': '/teacher/'}]
     user = User.objects.filter(name=request.session['name']).first()
     return render_to_response('teacher_info.html', locals())


def teacher_course(request):
     links = [{'name': '首页', 'page': '/'}, {'name': '教师页面', 'page': '/teacher/'}]
     user = User.objects.filter(name=request.session['name']).first()
     courses = ['C++', 'Java']
     return render_to_response('teacher_course.html', locals())
