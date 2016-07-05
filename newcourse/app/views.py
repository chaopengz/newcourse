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

def logout(request):
    del request.session['name']
    del request.session['type']
    return HttpResponseRedirect('/login/')


def file_download(request):
    filename = "1.doc"
    f = open(filename)
    data = f.read()
    f.close()

    response = HttpResponse(data)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response



