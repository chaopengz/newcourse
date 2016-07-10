# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import loader, context, RequestContext
import MySQLdb, json
from models import *
import datetime, calendar
import os
import time
import random
import csv
import sys
from view_auth_manage import *
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your views here.

def main(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    list_num = 2
    page_name = '课程管理'
    links = [{'name': '课程管理', 'page': '/administrator/course/'}]
    user = User.objects.filter(name=request.session['name']).first()
    courses = Course.objects.all()
    terms = Term.objects.all()
    res = []
    for course in courses:
        isrun = compare_time(course.start_date, course.end_date)
        course.start_date = course.start_date.strftime("%Y年%m月%d日");
        course.end_date = course.end_date.strftime("%Y年%m月%d日");
        res.append(CourseShow(course, isrun))
    return render_to_response('administrator_course.html', locals())


class CourseShow:
    def __init__(self, course, isrun):
        self.course = course
        self.isrun = isrun


# 比较课程的起止日期与系统当前日期，从而返回该课程是否已经结束
def compare_time(time1, time2):
    nowtime = datetime.date.today()
    print (time2 - nowtime).days
    if (nowtime - time1).days > 0 and (time2 - nowtime).days > 0:
        return True
    else:
        return False


def courseInfo(request, courseId):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    list_num = 2
    page_name = '课程详情'
    links = [{'name': '课程管理', 'page': '/administrator/course/'},
             {'name': '课程详情', 'page': '/administrator/course/courseInfo/' + courseId}]
    user = User.objects.filter(name=request.session['name']).first()
    course = Course.objects.filter(id=courseId).first()
    isrun = compare_time(course.start_date, course.end_date)
    course.start_date = course.start_date.strftime("%Y年%m月%d日")
    course.end_date = course.end_date.strftime("%Y年%m月%d日")
    res = CourseShow(course, isrun)
    teacher = User.objects.filter(id=course.teacher_id).first()
    term = Term.objects.filter(id=course.term_id).first()
    term.start_date = term.start_date.strftime("%Y年%m月%d日")
    term.end_date = term.end_date.strftime("%Y年%m月%d日")
    return render_to_response('administrator_courseInfo.html', locals())


def addCourseShow(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    list_num = 2
    page_name = '添加课程'
    links = [{'name': '课程管理', 'page': '/administrator/course/'},
             {'name': '添加课程', 'page': '/administrator/course/add_course'}]
    user = User.objects.get(name=request.session['name'])
    # 下拉列表的东西
    teachers = User.objects.filter(type=3)
    terms = Term.objects.all()
    # terms=Term.objects.filter(start_date__lte=datetime.date.today()).filter(end_date__gte=datetime.date.today())

    return render_to_response('administrator_add_course.html', locals())

def add_course_many(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    if 'infolist' in request.FILES:
        file = request.FILES.get('infolist', None)
        filedata=file.read()
        basename=str(time.time()).replace('.','_')+str(random.randrange(0,99999,1))
        path='%s/uploads/' % (os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media'))
        # 如果文件夹不存在，创建文件夹
        if not os.path.exists(path):
            os.makedirs(path)
        fullpath=path+basename
        f = open(fullpath, 'wb')
        f.write(filedata)
        f.close()
        error_list=[]
        term_id=request.POST.get('term_id')
        with open(fullpath,'rb') as f:
            reader = csv.reader(f)
            rownum=0
            for row in reader:
                rownum+=1
                if rownum>1:
                    if Course.objects.filter(name=row[0].decode('gb2312')).count() == 0:
                        try:
                            User.objects.get(name=row[2].decode('gb2312'),type=3)
                        except User.DoesNotExist:
                            error_list.append(row)
                            continue
                        else:
                            tid=User.objects.get(name=row[2].decode('gb2312'),type=3).id
                            if row[5].decode('gb2312')==u'是':
                                is_s=False
                            else:
                                is_s=True
                            date_format='%Y年%m月%d日'
                            date_format=date_format.decode('utf-8')
                            new_course=Course(
                                name=row[0].decode('gb2312'),
                                introduction=row[1].decode('gb2312'),
                                teacher_id=tid,
                                start_date=datetime.datetime.strptime(row[3].decode('gb2312'), date_format),
                                end_date=datetime.datetime.strptime(row[4].decode('gb2312'), date_format),
                                is_single=is_s,
                                term_id=term_id
                            )
                            new_course.save()
        os.remove(fullpath)
        for row in error_list:
            row[0]=row[0].decode('gb2312')
            row[1]=row[1].decode('gb2312')
            row[2]=row[2].decode('gb2312')
            row[3]=row[3].decode('gb2312')
            row[4]=row[4].decode('gb2312')
            row[5]=row[5].decode('gb2312')
        response_data = {}
        response_data['error_info'] = 'success'
        response_data['error_list'] = error_list
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data = {}
        response_data['error_info'] = 'failed'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

def changeCourseShow(request, courseId):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    list_num = 2
    page_name = '添加课程'
    links = [{'name': '课程管理', 'page': '/administrator/course/'},
             {'name': '添加课程', 'page': '/administrator/course/change_course/' + courseId}]
    user = User.objects.get(name=request.session['name'])

    course = Course.objects.get(id=courseId)
    # 更改日期格式便于显示在日期框里
    course.start_date = course.start_date.strftime("%m/%d/%Y")
    course.end_date = course.end_date.strftime("%m/%d/%Y")
    # 课程所对应信息
    teacher = User.objects.get(id=course.teacher_id)
    term = Term.objects.get(id=course.term_id)
    # 下拉列表的东西
    teachers = User.objects.filter(type=3)
    terms = Term.objects.all()
    # terms=Term.objects.filter(start_date__lte=datetime.date.today()).filter(end_date__gte=datetime.date.today())
    return render_to_response('administrator_change_course.html', locals())


def save_course(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)

    tname = request.POST['t_name']
    tintroduction = request.POST['t_introduction']
    tteacher = request.POST['t_teacher']
    tterm = request.POST['t_term']
    if request.POST['t_is_single'] == 2:
        tis_single = 0
    else:
        tis_single = 1
    tdate = request.POST['t_date']
    sdatestr = tdate[0:10]
    edatestr = tdate[13:23]
    sdate = datetime.datetime.strptime(sdatestr, "%m/%d/%Y").date()
    edate = datetime.datetime.strptime(edatestr, "%m/%d/%Y").date()

    if request.POST.get('t_id'):
        course = Course.objects.get(id=request.POST.get('t_id'))
        course.name = tname
        course.introduction = tintroduction
        course.teacher_id = tteacher
        course.term_id = tterm
        course.is_single = tis_single
        course.start_date = sdate
        course.end_date = edate
        course.save()
    else:
        course = Course(
            name=tname,
            introduction=tintroduction,
            teacher_id=tteacher,
            term_id=tterm,
            is_single=tis_single,
            start_date=sdate,
            end_date=edate
        )
        course.save()

    return HttpResponseRedirect('/administrator/course/courseInfo/' + str(course.id))

def delete_course(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    if 'c_id' in request.POST:
        cid=request.POST['c_id']
        try:
            course=Course.objects.filter(id=cid).first()
            course.delete()
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

def student(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    if 'cid' in request.GET:
        list_num = 2
        page_name = '选课学生管理'
        links = [{'name': '课程管理', 'page': '/administrator/course/'}, {'name': '选课学生管理', 'page': '#'}]
        user = User.objects.filter(name=request.session['name']).first()

        cid = request.GET.get('cid')
        course = Course.objects.get(id=cid)

        allstudents = User.objects.filter(type=2).order_by('name')
        students = []
        studentids = UserCourse.objects.filter(course=Course.objects.get(id=cid)).order_by('user')
        for s in studentids:
            students.append(s.user)

        return render_to_response('administrator_course_add_student.html', locals())
    else:
        return HttpResponseRedirect('/administrator/course/')


def add_student(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    if 'cid' in request.GET:
        cid = request.GET.get('cid')
        sid = request.GET.get('sid')
        try:
            course = Course.objects.filter(id=cid).first()
            student = User.objects.filter(id=sid).first()
        except:
            return HttpResponseRedirect('/administrator/course/student/?cid=' + cid)
        if student != None:
            try:
                UserCourse.objects.get(user=student, course=course)
            except UserCourse.DoesNotExist:
                uc = UserCourse(
                    user=student,
                    course=course
                )
                uc.save()
        return HttpResponseRedirect('/administrator/course/student/?cid=' + cid)
    else:
        return HttpResponseRedirect('/administrator/course/')

def add_course_select_many(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    if 'infolist' in request.FILES:
        file = request.FILES.get('infolist', None)
        filedata=file.read()
        basename=str(time.time()).replace('.','_')+str(random.randrange(0,99999,1))
        path='%s/uploads/' % (os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media'))
        # 如果文件夹不存在，创建文件夹
        if not os.path.exists(path):
            os.makedirs(path)
        fullpath=path+basename
        f = open(fullpath, 'wb')
        f.write(filedata)
        f.close()
        error_list=[]
        cid=request.POST.get('course_id')
        course=Course.objects.get(id=cid)
        with open(fullpath,'rb') as f:
            reader = csv.reader(f)
            rownum=0
            for row in reader:
                rownum+=1
                if rownum>1:
                    try:
                        # 是否有此学生
                        User.objects.get(name=row[0].decode('gb2312'),type=2)
                    except:
                        error_list.append(row)
                        continue

                    student=User.objects.get(name=row[0].decode('gb2312'),type=2)

                    try:
                        # 是否已经有这条选课记录
                        UserCourse.objects.get(user=student,course=course)
                    except:
                         # 选课
                        new_course_select=UserCourse(
                            user=student,
                            course=course
                        )
                        new_course_select.save()
                        continue
        os.remove(fullpath)
        for row in error_list:
            row[0]=row[0].decode('gb2312')
        response_data = {}
        response_data['error_info'] = 'success'
        response_data['error_list'] = error_list
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data = {}
        response_data['error_info'] = 'failed'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

def remove_student(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '1'): return jump_no_auth(request)
    if 'cid' in request.GET:
        cid = request.GET.get('cid')
        sid = request.GET.get('sid')
        try:
            course = Course.objects.filter(id=cid).first()
            student = User.objects.filter(id=sid).first()
        except:
            return HttpResponseRedirect('/administrator/course/student/?cid=' + cid)
        if student != None:
            try:
                uc = UserCourse.objects.filter(user=student, course=course).first()
                uc.delete()
            except:
                return HttpResponseRedirect('/administrator/course/student/?cid=' + cid)
        return HttpResponseRedirect('/administrator/course/student/?cid=' + cid)
    else:
        return HttpResponseRedirect('/administrator/course/')
