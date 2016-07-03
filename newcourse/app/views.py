# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *


# Create your views here.
def index(request):
     return render_to_response('index.html')


def login(request):
     if request.method == 'GET':
          return render_to_response('login.html')
     else:
          name = request.POST['username']
          password = request.POST['password']
          user=User.objects.filter(name=name, password=password)
          if user is []:
                return HttpResponseRedirect('/login/')
          else:
                request.session['name'] = name
                request.session['type'] = user[0].type
                if user[0].type == 1:
                     return HttpResponseRedirect('/administrator/')
                if user[0].type == 2:
                    return HttpResponseRedirect('/student/')
                if user[0].type == 3:
                     return HttpResponseRedirect('/teacher/')


def student(request):
     links=[{'name': '首页', 'page': '/'}, {'name': '学生页面', 'page': '/student/'} ]
     if 'name' in request.session:
          name = request.session['name']
          user=User.objects.filter(name=name).first()
          if user is not None:
               return render_to_response('student.html', locals())
     return HttpResponseRedirect('/login/')


def teacher(request):
     links=[{'name': '首页', 'page': '/'}, {'name': '教师页面', 'page': '/teacher/'} ]
     if 'name' in request.session:
          name = request.session['name']
          user=User.objects.filter(name=name).first()
          if user is not None:
               return render_to_response('teacher.html', locals())
     return HttpResponseRedirect('/login/')


def administrator(request):
     links=[{'name': '首页', 'page': '/'}, {'name': '教务管理员页面', 'page': '/administrator/'} ]
     if 'name' in request.session:
          name = request.session['name']
          user=User.objects.filter(name=name).first()
          if user is not None:
               return render_to_response('administrator.html', locals())
     return HttpResponseRedirect('/login/')
