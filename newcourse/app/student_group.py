# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import loader, context, RequestContext
import MySQLdb
from models import *
from django import forms


def addGroup(request):
    if request.method == 'POST':
        user = User.objects.filter(name=request.session['name']).first()
        name = request.POST['g_name']
        maxNum = request.POST['max']
        g = Group(name=name, max_number=maxNum, leader=user)
        g.save()
        return render_to_response('student_group.html')
    else:
        return render_to_response('student_add_group.html')
