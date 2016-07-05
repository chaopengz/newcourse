# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *
import time
from datetime import datetime
def modifyTerm(request):
    if request.method == 'POST':
        name = request.POST['name']
        week = request.POST['week']
        start = request.POST['start']
        end = request.POST['end']

        term = Term.objects.filter(id="1").first()
        term.name = name
        term.week = week

        start_m = start[0:2]
        start_d = start[3:5]
        start_y = start[6:]

        end_m = end[0:2]
        end_d = end[3:5]
        end_y = end[6:]

        term.start_date =start_y + '-' + start_m + '-' + start_d
        term.end_date = end_y + '-' + end_m + '-' + end_d
        term.save()
        return render_to_response('administrator_term.html', locals())
    else:
        list_num = 1
        page_name = '学期管理'
        links=[{'name': '学期管理', 'page': '/term/'}]
        user=User.objects.filter(name=request.session['name']).first()
        return render_to_response('administrator_term.html', locals())
