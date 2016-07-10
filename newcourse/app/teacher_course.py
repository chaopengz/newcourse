# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import *
from django.template import loader,context, RequestContext
import MySQLdb,json
from models import *
import datetime, calendar
from django import forms
import os, tempfile, zipfile
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from view_auth_manage import *
# Create your views here.


class CourseShow:
    def __init__(self,course,isrun):
        self.course=course
        self.isrun=isrun

# 比较课程的起止日期与系统当前日期，从而返回该课程是否已经结束
def compare_time(time1,time2):
    nowtime=datetime.date.today()
    print (time2-nowtime).days
    if (nowtime - time1).days > 0 and (time2-nowtime).days>0:
        return 0
    else:
        return 1

def course_teacher_info(request, courseId):
     if not judge_login(request): return jump_not_login(request)
     if not judge_auth(request, '3'): return jump_no_auth(request)
     page_name = '课程详情'
     request.session['course_id'] = courseId

     course_id = int(request.session['course_id'])
     course = Course.objects.get(id=course_id)
     links=[{'name': '课程管理', 'page': '/teacher/course/'} ,{'name':course.name,'page': '/teacher/course'}]
     user=User.objects.filter(name=request.session['name']).first()
     course=Course.objects.filter(id=courseId).first()
     teacher=User.objects.filter(id=course.teacher_id).first()
     term=Term.objects.filter(id=course.term_id).first()
     coursegroups = GroupCourse.objects.filter(course=course)
     # groups = Group.objects.filter(id in GroupCourse.objects.filter(course=course).values('group'))
     groups = [Group.objects.get(pk = u.group_id) for u in coursegroups]
     isrun=compare_time(course.start_date, course.end_date)
     res = CourseShow(course,isrun)
     course.start_date = course.start_date.strftime("%Y年%m月%d日")
     course.end_date = course.end_date.strftime("%Y年%m月%d日")
     return render_to_response('teacher_course.html', locals())


def course_resource(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '3'): return jump_no_auth(request)
    list_num = 2
    page_name = '资源列表'
    course_id = int(request.session['course_id'])
    course = Course.objects.get(id=course_id)
    links = [{'name': '课程管理', 'page': '/teacher/course'}, {'name':course.name,'page': '/teacher/course'},
             {'name': '资源管理', 'page': '/teacher/course/resource'}]
    user = User.objects.filter(name=request.session['name']).first()
    course_id = int(request.session['course_id'])
    user = User.objects.filter(name=request.session['name']).first()
    resource_classes = ResourceClass.objects.all()
    resources = Resource.objects.filter(course_id=course_id)
    for resource in resources:
        resource.submit_time = resource.submit_time.strftime("%Y年%m月%d日%H时%M分")
    finish = compare_time(course.start_date, course.end_date)
    return render_to_response('teacher_course_resource.html', locals())

class UserForm(forms.Form):
    Description = forms.CharField(label='资源名称')
    File = forms.FileField(label='文件位置')

def course_resource_publish(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '3'): return jump_no_auth(request)
    list_num = 2
    user = User.objects.filter(name=request.session['name']).first()
    page_name = '资源列表'
    course_id = int(request.session['course_id'])
    course=Course.objects.get(id=course_id)
    links = [{'name': '课程管理', 'page': '/teacher/course'}, {'name':course.name,'page': '/teacher/course'},
             {'name': '资源管理', 'page': '/teacher/course/resource'},
             {'name': '发布资源', 'page': '/teacher/course/resource/resource_publish'} ]
    course_id = int(request.session['course_id'])
    resources = Resource.objects.filter(course_id=course_id)
    user=User.objects.filter(name=request.session['name']).first()
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            # 获取表单信息
            description = uf.cleaned_data['Description']
            filepath = uf.cleaned_data['File']
            # 写入数据库
            resource = Resource()
            resource_class = ResourceClass.objects.get(pk=1)
            resource.name = description
            resource.server_path = filepath
            resource.resource_class = resource_class
            resource.course_id = course_id
            resource.save()

            course_id = int(request.session['course_id'])
            resources = Resource.objects.filter(course_id=course_id)
            return HttpResponseRedirect('/teacher/course/resource/')
    else:
        uf = UserForm()

    return render_to_response('teacher_course_resource_publish.html', locals())


def course_resource_class(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '3'): return jump_no_auth(request)
    id = request.POST['resource_id']
    resource_class_id = request.POST['resource_class']
    resource = Resource.objects.get(pk=id)
    resource_class = ResourceClass.objects.get(pk=resource_class_id)
    resource.resource_class = resource_class
    resource.save()
    return HttpResponse(json.dumps(True))


def course_resource_class_add(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '3'): return jump_no_auth(request)
    name = request.POST['resource_class_name']
    resource_class = ResourceClass()
    resource_class.name = name
    resource_class.save()
    return HttpResponse(json.dumps(True))

def group_delete(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '3'): return jump_no_auth(request)
    # usergroup=UserGroup.objects.get(pk=request.POST['groupid'])
    # taskfile.delete()
    return HttpResponse(json.dumps(True))

def course_task(request):
     if not judge_login(request): return jump_not_login(request)
     if not judge_auth(request, '3'): return jump_no_auth(request)
     list_num = 1
     page_name = '作业列表'
     course_id = int(request.session['course_id'])
     course = Course.objects.get(id=course_id)
     links=[{'name': '课程管理', 'page': '/teacher/course'} , {'name':course.name,'page': '/teacher/course'},
            {'name': '作业管理', 'page': '/teacher/course/task'}]
     user=User.objects.filter(name=request.session['name']).first()
     course_id=int(request.session['course_id'])
     tasks=TaskRequirement.objects.filter(course_id=course_id)
     finish = compare_time(course.start_date, course.end_date)
     for task in tasks:
         task.start_date = task.start_date.strftime("%Y年%m月%d日")
         task.end_date = task.end_date.strftime("%Y年%m月%d日")
     return render_to_response('teacher_course_task.html', locals())

def course_task_publish(request):
     if not judge_login(request): return jump_not_login(request)
     if not judge_auth(request, '3'): return jump_no_auth(request)
     list_num = 1
     page_name = '作业列表'
     course_id = int(request.session['course_id'])
     course = Course.objects.get(id=course_id)
     links=[{'name': '课程管理', 'page': '/teacher/course'} ,{'name':course.name,'page': '/teacher/course'},
            {'name': '作业管理', 'page': '/teacher/course/task'} ,
            {'name': '作业提交', 'page': '/teacher/course/task_publish'}]
     finish = compare_time(course.start_date,course.end_date)

     if request.method=='GET':
        user=User.objects.filter(name=request.session['name']).first()
        course_id=int(request.session['course_id'])
        return render_to_response('teacher_course_task_publish.html', locals())
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
        return HttpResponseRedirect('/teacher/course/task')


def course_task_info(request, task_id):
     if not judge_login(request): return jump_not_login(request)
     if not judge_auth(request, '3'): return jump_no_auth(request)
     list_num = 1
     page_name = '作业列表'
     course_id = int(request.session['course_id'])
     course = Course.objects.get(id=course_id)
     links = [{'name': '课程管理', 'page': '/teacher/course'} ,{'name':course.name,'page': '/teacher/course'},
              {'name': '作业管理', 'page': '/teacher/course/task'} ,
              {'name': '作业详情', 'page': '/teacher/course/task_info'}]
     user = User.objects.filter(name=request.session['name']).first()
     course_id = int(request.session['course_id'])
     course=Course.objects.filter(id=course_id).first()
     teacher=User.objects.filter(id=course.teacher_id).first()
     term=Term.objects.filter(id=course.term_id).first()
     task = TaskRequirement.objects.get(pk=task_id)
     task.start_date = task.start_date.strftime("%Y年%m月%d日")
     task.end_date = task.end_date.strftime("%Y年%m月%d日")
     task_file =task.taskfile_set.all()
     for tf in task_file:
            tf.submit_time = tf.submit_time.strftime("%Y年%m月%d日%H时%M分")
     request.session['task_id'] = task_id
     return render_to_response('teacher_course_task_info.html', locals())

def course_task_grade(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '3'): return jump_no_auth(request)
    id = request.POST['task_id']
    grade = request.POST['grade']
    task_file = TaskFile.objects.get(pk=id)
    task_file.grade=grade
    task_file.save()
    return HttpResponse(json.dumps(True))


def course_task_grade_many(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '3'): return jump_no_auth(request)
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
        task_id= request.session['task_id']
        with open(fullpath,'rb') as f:
            reader = csv.reader(f)
            rownum=0
            for row in reader:
                rownum+=1
                if rownum>1:
                    if len(User.objects.filter(name=row[0].decode('gb2312'))) == 0:
                        try:
                            User.objects.get(name=row[0].decode('gb2312'))
                        except User.DoesNotExist:
                            error_list.append(row)
                            continue
                    else:
                        user_temp = User.objects.filter(name=row[0].decode('gb2312')).first()
                        if len(TaskFile.objects.filter(task_requirement_id=task_id, user=user_temp))==0:
                            error_list.append(row)
                            continue
                        else:
                            task_file = TaskFile.objects.filter(task_requirement_id=task_id, user=user_temp).first()
                            task_file.grade = row[1]
                            task_file.comment = row[2].decode('gb2312')
                            task_file.save()
        os.remove(fullpath)
        for row in error_list:
            row[0]=row[0].decode('gb2312')
            row[1]=row[1].decode('gb2312')
            row[2]=row[2].decode('gb2312')
        response_data = {}
        response_data['error_info'] = 'success'
        response_data['error_list'] = error_list
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data = {}
        response_data['error_info'] = 'failed'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def course_task_comment(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '3'): return jump_no_auth(request)
    id = request.POST['task_id']
    commnet = request.POST['comment']
    task_file = TaskFile.objects.get(pk=id)
    task_file.comment = commnet
    task_file.save()
    return HttpResponse(json.dumps(True))


def course_task_content(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '3'): return jump_no_auth(request)
    id = request.POST['task_id']
    task_file = TaskFile.objects.get(pk=id)
    return HttpResponse(json.dumps(task_file.content))


def group_accept(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '3'): return jump_no_auth(request)
    id = request.POST['course_group_id']
    course_group = GroupCourse.objects.get(pk=id)
    course_group.is_allowed = 1
    course_group.save()
    return HttpResponse(json.dumps(True))


def group_refuse(request):
    if not judge_login(request): return jump_not_login(request)
    if not judge_auth(request, '3'): return jump_no_auth(request)
    id = request.POST['course_group_id']
    course_group = GroupCourse.objects.get(pk=id)
    course_group.is_allowed = 2
    course_group.save()
    return HttpResponse(json.dumps(True))


def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()


def one_click_download(request):
    judge_auth(request,'3')
    user = User.objects.filter(name=request.session['name']).first()
    course_id = request.session['course_id']
    task_id = request.session['task_id']
    dir = '/media/task/' + course_id + '/' + task_id
    file = '/media/temp.zip'
    root_dir = os.path.dirname(__file__)
    zip_dir(root_dir[:-4] + dir, root_dir[:-4] + file)
    return HttpResponseRedirect(file)


def file_download(request, filename):
    judge_auth(request,'3')
    f = open('media/' + filename)
    data = f.read()
    f.close()
    response = HttpResponse(data)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

def resourcedelete(request):
    judge_auth(request,'3')
    resource=Resource.objects.get(pk=request.POST['resourceid'])
    resource.delete()
    return HttpResponse(json.dumps(True))