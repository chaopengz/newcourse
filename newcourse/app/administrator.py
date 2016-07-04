# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *


# Create your views here.
def administrator(request):
     page_name='教务首页'
     links=[ {'name': '教务管理员页面', 'page': '/administrator/'} ]
     if 'name' in request.session:
          name = request.session['name']
          user=User.objects.filter(name=name).first()
          if user is not None:
               return render_to_response('administrator.html', locals())
     return HttpResponseRedirect('/login/')