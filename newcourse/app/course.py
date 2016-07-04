# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb
from models import *
import datetime, calendar
from django import forms
# Create your views here.

def main(request):
     list_num=2
     page_name='课程管理'
     links=[ {'name': '课程管理', 'page': '/course/'} ]
     user=User.objects.filter(name=request.session['name']).first()
     courses=Course.objects.all()
     res=[]
     for course in courses:
         isrun=compare_time(course.start_date, course.end_date)
         course.start_date=course.start_date.strftime("%Y年%m月%d日");
         course.end_date=course.end_date.strftime("%Y年%m月%d日");
         res.append(CourseShow(course,isrun))
     return render_to_response('administrator_course.html', locals())


class CourseShow:
    def __init__(self,course,isrun):
        self.course=course
        self.isrun=isrun

# 比较课程的起止日期与系统当前日期，从而返回该课程是否已经结束
def compare_time(time1,time2):
    nowtime=datetime.date.today()
    print (time2-nowtime).days
    if (nowtime - time1).days > 0 and (time2-nowtime).days>0:
        return True
    else:
        return False


def courseInfo(request, courseId):
     list_num = 2
     page_name = '课程详情'
     links=[{'name': '课程管理', 'page': '/course/'} , {'name': '课程详情', 'page': '/course/courseInfo/'+courseId}]
     user=User.objects.filter(name=request.session['name']).first()
     course=Course.objects.filter(id=courseId).first()
     isrun=compare_time(course.start_date, course.end_date)
     course.start_date=course.start_date.strftime("%Y年%m月%d日")
     course.end_date=course.end_date.strftime("%Y年%m月%d日")
     res = CourseShow(course,isrun)
     teacher=User.objects.filter(id=course.teacher_id).first()
     term=Term.objects.filter(id=course.term_id).first()
     term.start_date=term.start_date.strftime("%Y年%m月%d日")
     term.end_date=term.end_date.strftime("%Y年%m月%d日")
     return render_to_response('administrator_courseInfo.html', locals())

def addCourseShow(request):
    list_num = 2
    page_name = '添加课程'
    links=[{'name': '课程管理', 'page': '/course/'} , {'name': '添加课程', 'page': '/course/add_course'}]
    user=User.objects.get(name=request.session['name'])
    #下拉列表的东西
    teachers=User.objects.filter(type=3)
    terms=Term.objects.filter(start_date__lte=datetime.date.today()).filter(end_date__gte=datetime.date.today())

    return render_to_response('add_course.html', locals())

def changeCourseShow(request,courseId):
    list_num = 2
    page_name = '添加课程'
    links=[{'name': '课程管理', 'page': '/course/'} , {'name': '添加课程', 'page': '/course/change_course/'+courseId}]
    user=User.objects.get(name=request.session['name'])

    course=Course.objects.get(id=courseId)
    #更改日期格式便于显示在日期框里
    course.start_date=course.start_date.strftime("%m/%d/%Y")
    course.end_date=course.end_date.strftime("%m/%d/%Y")
    #课程所对应信息
    teacher=User.objects.get(id=course.teacher_id)
    term=Term.objects.get(id=course.term_id)
    #下拉列表的东西
    teachers=User.objects.filter(type=3)
    terms=Term.objects.filter(start_date__lte=datetime.date.today()).filter(end_date__gte=datetime.date.today())
    return render_to_response('change_course.html', locals())

def save_course(request):
    list_num = 2
    page_name = '课程详情'
    links=[{'name': '课程管理', 'page': '/course/'} , {'name': '课程详情', 'page': '/course/courseInfo/'}]
    user=User.objects.filter(name=request.session['name']).first()

    tname=request.POST['t_name']
    tintroduction=request.POST['t_introduction']
    tteacher=request.POST['t_teacher']
    tterm=request.POST['t_term']
    if request.POST['t_is_single'] == 2:
        tis_single=0
    else:
        tis_single=1
    tdate=request.POST['t_date']
    sdatestr=tdate[0:10]
    edatestr=tdate[13:23]
    sdate=datetime.datetime.strptime(sdatestr, "%m/%d/%Y").date()
    edate=datetime.datetime.strptime(edatestr, "%m/%d/%Y").date()

    if request.POST.get('t_id'):
        course=Course.objects.get(id=request.POST.get('t_id'))
        course.name=tname
        course.introduction=tintroduction
        course.teacher_id=tteacher
        course.term_id=tterm
        course.is_single=tis_single
        course.start_date=sdate
        course.end_date=edate
        course.save()
    else:
        course=Course(
            name=tname,
            introduction=tintroduction,
            teacher_id=tteacher,
            term_id=tterm,
            is_single=tis_single,
            start_date=sdate,
            end_date=edate
         )
        course.save()

    return HttpResponseRedirect('/course/courseInfo/'+str(course.id))

def course_teacher_info(request, courseId):
     page_name = '课程详情'
     links=[{'name': '课程管理', 'page': '/course/'} ]
     request.session['course_id'] = courseId
     user=User.objects.filter(name=request.session['name']).first()
     course=Course.objects.filter(id=courseId).first()
     teacher=User.objects.filter(id=course.teacher_id).first()
     term=Term.objects.filter(id=course.term_id).first()
     isrun=compare_time(course.start_date, course.end_date)
     res = CourseShow(course,isrun)
     return render_to_response('course.html', locals())


def course_resource(request):
    list_num = 2
    page_name = '资源列表'
    links = [{'name': '课程管理', 'page': '/course'}, {'name': '资源管理', 'page': '/course/resource'}]
    course_id = int(request.session['course_id'])
    resources = Resource.objects.filter(course_id=course_id)
    return render_to_response('course_resource.html', locals())

class UserForm(forms.Form):
    Description = forms.CharField(label='资源名称')
    Folder = forms.CharField(label='文件夹名称')
    File = forms.FileField(label='文件位置')

def course_resource_publish(request):
    list_num = 2
    page_name = '资源列表'
    links = [{'name': '课程管理', 'page': '/course'}, {'name': '资源管理', 'page': '/course/resource'},
             {'name': '发布资源', 'page': '/course/resource/resource_publish'} ]
    course_id = int(request.session['course_id'])
    resources = Resource.objects.filter(course_id=course_id)

    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            # 获取表单信息
            description = uf.cleaned_data['Description']
            filepath = uf.cleaned_data['File']
            folder=uf.cleaned_data['Folder']
            # 写入数据库
            resource = Resource()
            resource.name = description
            resource.server_path = filepath
            resource.directory = folder
            resource.course_id = course_id
            resource.save()
            return HttpResponse('upload ok!')
    else:
        uf = UserForm()

    return render_to_response('course_resource_publish.html', locals())

def course_task(request):
     list_num = 1
     page_name = '作业列表'
     links=[{'name': '课程管理', 'page': '/course'} , {'name': '作业管理', 'page': '/course/task'}]
     user=User.objects.filter(name=request.session['name']).first()
     course_id=int(request.session['course_id'])
     tasks=TaskRequirement.objects.filter(course_id=course_id)
     return render_to_response('course_task.html', locals())


def course_task_publish(request):
     list_num = 1
     page_name = '作业列表'
     links=[{'name': '课程管理', 'page': '/course'} ,{'name': '作业管理', 'page': '/course/task'} ,
            {'name': '作业提交', 'page': '/course/task_publish'}]
     if request.method=='GET':
        user=User.objects.filter(name=request.session['name']).first()
        course_id=int(request.session['course_id'])
        return render_to_response('course_task_publish.html', locals())
     else:
        task = TaskRequirement()
        task.name = request.POST['name']
        task.base_requirements = request.POST['requirements']
        course_id = int(request.session['course_id'])
        course = Course.objects.filter(id=course_id).first()
        task.is_single = course.is_single
        task.course = course
        start = request.POST['start']
        end = request.POST['end']
        start_m = start[0:2]
        start_d = start[3:5]
        start_y = start[6:]
        end_m = end[0:2]
        end_d = end[3:5]
        end_y = end[6:]
        task.start_date =start_y + '-' + start_m + '-' + start_d
        task.end_date = end_y + '-' + end_m + '-' + end_d
        task.save()
        return render_to_response('course_task.html', locals())


def course_task_info(request, task_id):
     list_num = 1
     page_name = '作业列表'
     links = [{'name': '课程管理', 'page': '/course'} ,{'name': '作业管理', 'page': '/course/task'} ,
              {'name': '作业详情', 'page': '/course/task_info'}]
     user = User.objects.filter(name=request.session['name']).first()
     course_id = int(request.session['course_id'])
     course=Course.objects.filter(id=course_id).first()
     teacher=User.objects.filter(id=course.teacher_id).first()
     term=Term.objects.filter(id=course.term_id).first()
     task = TaskRequirement.objects.get(pk=task_id)
     task_file =task.taskfile_set.all()
     return render_to_response('course_task_info.html', locals())