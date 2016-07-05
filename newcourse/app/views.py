# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *
import json

# Create your views here.
def index(request):
     return render_to_response('index.html')


def login(request):
     if 'name' in request.session:
         user=User.objects.filter(name=request.session['name'])
         if user[0].type == 1:
              return HttpResponseRedirect('/administrator/')
         if user[0].type == 2:
              return HttpResponseRedirect('/student/')
         if user[0].type == 3:
              return HttpResponseRedirect('/teacher/')
     if request.method == 'GET':
          return render_to_response('login.html')
     else:
          name = request.POST['username']
          password = request.POST['password']
          user=User.objects.get(name=name, password=password)
          if user is None:
                return render_to_response('/')
          else:
                request.session['name'] = name
                request.session['type'] = user.type
                if user.type == 1:
                     return HttpResponseRedirect('/administrator/')
                if user.type == 2:
                    return HttpResponseRedirect('/student/')
                if user.type == 3:
                     return HttpResponseRedirect('/teacher/')

def logout(request):
    del request.session['name']
    del request.session['type']
    return HttpResponseRedirect('/login/')

def change_password(request):
    if 'name' in request.session:
        user=User.objects.get(name=request.session['name'])
        if 't_oldpw' in request.POST:
            #修改密码
            if request.POST.get('t_oldpw') == user.password:
                #改密码
                is_success='1'
                user.password=request.POST.get('t_newpw')
                user.save()
            else:
                #旧密码输错
                is_success='0'
        else:
            #get方法，返回修改页
            page_name = '课程详情'
            links=[{'name': '修改密码', 'page': '/change_password/'} ]
            user=User.objects.filter(name=request.session['name']).first()
        return render_to_response('change_password.html', locals())
    else:
        return HttpResponseRedirect('/login/')




