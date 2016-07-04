# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *


# Create your views here.
def student(request):
     links=[{'name': '首页', 'page': '/'}, {'name': '学生页面', 'page': '/student/'} ]
     if 'name' in request.session:
          name = request.session['name']
          user=User.objects.filter(name=name).first()
          if user is not None:
               return render_to_response('student.html', locals())
     return HttpResponseRedirect('/login/')


def student_info(request):
     links=[{'name': '首页', 'page': '/'}, {'name': '学生页面', 'page': '/student/'} ]
     user=User.objects.filter(name=request.session['name']).first()
     return render_to_response('student_info.html', locals())


def student_course(request):
     links=[{'name': '首页', 'page': '/'}, {'name': '学生页面', 'page': '/student/'} ]
     user=User.objects.filter(name=request.session['name']).first()
     courses=['C++', 'Java']
     return render_to_response('student_course.html', locals())


def student_group(request):
     links=[{'name': '首页', 'page': '/'}, {'name': '学生页面', 'page': '/student/'} ]
     user=User.objects.filter(name=request.session['name']).first()
     groups=['534team', 'new course']
     return render_to_response('student_group.html', locals())