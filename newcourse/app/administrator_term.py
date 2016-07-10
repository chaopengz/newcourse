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
from view_auth_manage import *

def modifyTerm(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
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
        links=[{'name': '学期管理', 'page': '/administrator/term/'},{'name':'添加学期','page':'/administrator/term/add_term'}]
        user=User.objects.filter(name=request.session['name']).first()
        return render_to_response('administrator_add_term.html', locals())


def main(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
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

# 比较课程的起止日期与系统当前日期，从而返回该课程是否已经结束
def compare_time(time1, time2,cmptime=datetime.date.today()):
    print (time2 - cmptime).days
    if (cmptime - time1).days >= 0 and (time2 - cmptime).days >= 0:
        return True
    else:
        return False


class TermShow:
    def __init__(self,term,isrun):
        self.term=term
        self.isrun=isrun


def termInfo(request, termId):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
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
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
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
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)

    tname=request.POST['t_name']

    tdate=request.POST['t_date']
    sdatestr=tdate[0:10]
    edatestr=tdate[13:23]
    sdate=datetime.datetime.strptime(sdatestr, "%m/%d/%Y").date()
    edate=datetime.datetime.strptime(edatestr, "%m/%d/%Y").date()
    tweek=((edate-sdate).days)/7

    if request.POST.get('t_id'):
        # 修改
        term=Term.objects.get(id=request.POST.get('t_id'))
        term.name=tname
        term.start_date=sdate
        term.end_date=edate
        term.week=tweek
        term.save()
        return HttpResponseRedirect('/administrator/term/termInfo/'+str(term.id))
    else:
        # 新建
        term=Term(
            name=tname,
            week=tweek,
            start_date=sdate,
            end_date=edate
         )
        term.save()
        return HttpResponseRedirect('/administrator/term/')

def delete_term(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    if 't_id' in request.POST:
        tid=request.POST['t_id']
        try:
            term=Term.objects.filter(id=tid).first()
            term.delete()
            response_data = {}
            response_data['error_info'] = 'success'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except:
            response_data = {}
            response_data['error_info'] = 'failed'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    response_data = {}
    response_data['error_info'] = 'failed'
    return HttpResponse(json.dumps(response_data), content_type="application/json")