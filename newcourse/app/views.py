# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import *
from django.template import loader, context, RequestContext
import MySQLdb
from models import *
import json
import os
import random
import json
from PIL import Image
from view_auth_manage import *
# Create your views here.
def index(request):
    return render_to_response('index.html')


def login(request):
    if 'name' in request.session:
        # 已登录，则重定向
        user = User.objects.filter(name=request.session['name'])
        if user[0].type == 1:
            return HttpResponseRedirect('/administrator/')
        if user[0].type == 2:
            return HttpResponseRedirect('/student/')
        if user[0].type == 3:
            return HttpResponseRedirect('/teacher/')
    if request.method == 'GET':
        # 显示页面
        return render_to_response('login.html')
    else:
        # 登录
        name = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(name=name, password=password)
        except User.DoesNotExist:
            request.session['message'] = "用户名或密码错误，请重新登录"
            request.session['nexturl'] = "/login/"
            return HttpResponseRedirect('/info/')
        else:
            request.session['name'] = name
            request.session['type'] = user.type
            if user.type == 1:
                return HttpResponseRedirect('/administrator/')
            if user.type == 2:
                return HttpResponseRedirect('/student/')
            if user.type == 3:
                return HttpResponseRedirect('/teacher/')


def logout(request):
    del request.session['name']
    del request.session['type']
    request.session['message'] = "登出成功"
    request.session['nexturl'] = "/login/"
    return HttpResponseRedirect('/info/')

def userinfo(request):
    if not judge_login(request): return jump_not_login(request)
    page_name = '管理个人信息'
    links = [{'name': '管理个人信息', 'page': '#'}]
    user = User.objects.filter(name=request.session['name']).first()
    return render_to_response('userinfo.html', locals())

# 图片裁切
def deal_image(name,data):
    im = Image.open(name)
    im = im.rotate(data['rotate']*-1)
    # box = im.copy() #直接复制图像
    box = (int(data['x']), int(data['y']), int(data['width']+data['x']), int(data['height'] +data['y']))
    region = im.crop(box)
    # region = region.rotate(data['rotate']*-1)
    # im.paste(region, box)
    region.save(name,"gif")

def save_info(request):
    if not judge_login(request): return jump_not_login(request)
    if 'avatar_data' in request.POST:
        user = User.objects.get(name=request.session['name'])

        file = request.FILES.get('avatar_file', None)
        filedata=json.loads(request.POST.get('avatar_data'))
        # height width x y rotate
        aimage=file.read()
        # aimage = Image.open(file.name)
        ext=file.name.split('.')[-1]
        sub_folder_name=str(random.randint(0,10))
        path='%s/avatars/%s/' % (os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static') ,sub_folder_name)

        # 如果文件夹不存在，创建文件夹
        if not os.path.exists(path):
            os.makedirs(path)
        import time
        ext = ext.lower()
        basename=str(time.time()).replace('.','_')+str(random.randrange(0,99999,1))
        filename=basename+'.'+ext
        bfilename=basename+'.jpg'
        ret_filename='/static/avatars/%s/%s' % (sub_folder_name,bfilename)
        filename=path+filename
        filename=filename.lower()
        # 删除原图
        try:
            os.remove(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+user.pic)
        except:
            print 'file remove error'
        #直接保存原图
        imgfile = open(filename, 'wb')

        imgfile.write(aimage)
        imgfile.close()
        # 裁剪图片
        deal_image(filename,filedata)

        user.pic=ret_filename
        user.save()
        response_data = {}
        response_data['result'] = 'success'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    if 'realname' in request.POST:
        user = User.objects.get(name=request.session['name'])
        user.real_name = request.POST['realname']
        user.save()
    request.session['message'] = "保存个人信息成功"
    request.session['nexturl'] = "/"
    return HttpResponseRedirect('/info/')


def change_password(request):
    if not judge_login(request): return jump_not_login(request)
    if 'name' in request.session:
        user = User.objects.get(name=request.session['name'])
        if 't_oldpw' in request.POST:
            # 修改密码
            if request.POST.get('t_oldpw') == user.password:
                # 改密码
                user.password = request.POST.get('t_newpw')
                user.save()
                request.session['message'] = "密码修改成功。请重新登录。"
                request.session['nexturl'] = "/logout/"
            else:
                # 旧密码输错
                request.session['message'] = "旧密码输入错误，请重新确认。"
                request.session['nexturl'] = "/change_password/"
        else:
            # get方法，返回修改页
            page_name = '课程详情'
            links = [{'name': '修改密码', 'page': '/change_password/'}]
            user = User.objects.filter(name=request.session['name']).first()
            return render_to_response('change_password.html', locals())
        return HttpResponseRedirect('/info/')
    else:
        return HttpResponseRedirect('/login/')


def info(request):
    if 'message' in request.session:
        message = request.session['message']
        nexturl = request.session['nexturl']
    if 'name' in request.session:
        user = User.objects.get(name=request.session['name'])
        page_name = '提示信息'
        links = [{'name': '提示信息', 'page': '#'}]
    return render_to_response('info.html', locals())
