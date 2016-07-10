# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *
from view_auth_manage import *

# Create your views here.
def administrator(request):
     if not judge_login(request): return jump_not_login(request)
     if not judge_auth(request, '1'): return jump_no_auth(request)
     page_name='教务首页'
     links=[  ]
     if 'name' in request.session:
          name = request.session['name']
          user=User.objects.filter(name=name).first()
          if user is not None:
               return render_to_response('administrator.html', locals())
     return HttpResponseRedirect('/login/')