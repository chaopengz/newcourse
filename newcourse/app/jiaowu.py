# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *

def modifyTerm(request):
    list_num = 1
    page_name = '学期管理'
    links=[{'name': '学期管理', 'page': '/term/'}]
    user=User.objects.filter(name=request.session['name']).first()
    return render_to_response('jiaowu_term.html', locals())
