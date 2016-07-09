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

# 根据用户类型返回不同的用户对应的首页。
def get_mainpage(type):
    if type == 1:
        # 教务管理员
        return '/administrator/'
    if type == 2:
        # 学生
        return '/student/'
    if type == 3:
        # 教师
        return '/teacher/'

# 先到信息页，再跳转到指定url
# request - 传入的request对象
# message - 要显示的信息
# next_url - 将要跳转到的目标url
def jump_with_info(request,message,next_url):
    request.session['message'] = message
    request.session['nexturl'] = next_url
    return HttpResponseRedirect('/info/')

# 判断登录状态及访问权限，并且根据需要跳转到对应的页面
def judge_auth(request,type):
    if 'name' in request.session:
        # 已登录
        usertype=request.session['type']
        if usertype != type:
            # 角色不同，无法访问这个页面
            jump_with_info(request,"您无权访问这个页面。",get_mainpage(usertype))
    else:
        # 未登录
        jump_with_info(request,"您的登录状态已过期，请重新登录。","/login/")

# 判断是否登陆，没有就返回登录页
def judge_login(request):
    if 'name' in request.session:
        # 已登录
        return True
    else:
        # 未登录
        jump_with_info(request,"您的登录状态已过期，请重新登录。","/login/")