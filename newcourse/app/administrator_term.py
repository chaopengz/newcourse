# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *
import time
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb,json
from models import *
import datetime, calendar

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
        return render_to_response('jiaowu_term_success.html')
    else:
        list_num = 1
        page_name = '学期管理'
        links=[{'name': '学期管理', 'page': '/administrator/term/'},{'name':'添加学期','page':'/administrator/term/add_term'}]
        user=User.objects.filter(name=request.session['name']).first()
        return render_to_response('administrator_add_term.html', locals())



def main(request):
    list_num = 1
    page_name = '学期管理'
    links = [{'name': '学期管理', 'page': '/administrator/term/'}]
    user = User.objects.filter(name=request.session['name']).first()
    terms = Term.objects.all()
    res = []
    for term in terms:
        isrun = compare_time(term.start_date, term.end_date)
        term.start_date = term.start_date.strftime("%Y年%m月%d日");
        term.end_date = term.end_date.strftime("%Y年%m月%d日");
        res.append(TermShow(term, isrun))
    return render_to_response('administrator_term.html', locals())

# 比较学期的起止日期与系统当前日期，从而返回该学期是否已经结束
def compare_time(time1,time2):
    nowtime=datetime.date.today()
    if (nowtime - time1).days > 0 and (time2-nowtime).days>0:
        return True
    else:
        return False
class TermShow:
    def __init__(self,term,isrun):
        self.term=term
        self.isrun=isrun


def termInfo(request, termId):
    list_num = 1
    page_name = '学期详情'
    links = [{'name': '学期管理', 'page': '/administrator/term/'},
             {'name': '学期详情', 'page': '/administrator/term/termInfo/' + termId}]
    user = User.objects.filter(name=request.session['name']).first()
    term = Term.objects.filter(id=termId).first()
    isrun = compare_time(term.start_date, term.end_date)
    term.start_date = term.start_date.strftime("%Y年%m月%d日")
    term.end_date = term.end_date.strftime("%Y年%m月%d日")
    res = TermShow(term, isrun)
    return render_to_response('administrator_termInfo.html', locals())

def changeTermShow(request,termId):
    list_num = 1
    page_name = '修改学期'
    links=[{'name': '学期管理', 'page': '/administrator/term/'} , {'name': '修改学期', 'page': '/administrator/term/change_term/'+termId}]
    user=User.objects.get(name=request.session['name'])

    term=Term.objects.get(id=termId)
    #更改日期格式便于显示在日期框里
    term.start_date=term.start_date.strftime("%m/%d/%Y")
    term.end_date=term.end_date.strftime("%m/%d/%Y")

    return render_to_response('administrator_change_term.html', locals())

def save_term(request):
    list_num = 1
    page_name = '学期详情'
    links=[{'name': '学期管理', 'page': '/administrator/term/'} , {'name': '学期详情', 'page': '/administrator/term/termInfo/'}]
    user=User.objects.filter(name=request.session['name']).first()

    tname=request.POST['t_name']
    tweek=request.POST['t_week']
    tdate=request.POST['t_date']
    sdatestr=tdate[0:10]
    edatestr=tdate[13:23]
    sdate=datetime.datetime.strptime(sdatestr, "%m/%d/%Y").date()
    edate=datetime.datetime.strptime(edatestr, "%m/%d/%Y").date()

    if request.POST.get('t_id'):
        term=Term.objects.get(id=request.POST.get('t_id'))
        term.name=tname
        term.start_date=sdate
        term.end_date=edate
        term.save()
    else:
        term=Term(
            name=tname,
            start_date=sdate,
            end_date=edate
         )
        term.save()

    return HttpResponseRedirect('/administrator/term/termInfo/'+str(term.id))