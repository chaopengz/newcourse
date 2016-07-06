from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from models import *


def t_Home(request):
    courseId = request.session['course_id']
    c = Chat.objects.filter(courseid=courseId)
    return render(request, "teacher_course_message.html", {'chat': c})


def s_Home(request):
    print request.session
    courseId = 0
    if 'course_id' in request.session:
        courseId = request.session['course_id']
    c = Chat.objects.filter(courseid=courseId)
    return render(request, "student_course_message.html", {'chat': c})


def Post(request):
    if request.method == "POST":
        msg = request.POST['msgbox']
        user = User.objects.filter(name=request.session['name']).first()
        courseId = 0
        if 'course_id' in request.session:
            courseId = request.session['course_id']
        c = Chat(user=user, message=msg, courseid=courseId)
        if msg != '':
            c.save()
        return JsonResponse({'msg': msg, 'user': c.user.real_name})
    else:
        return HttpResponse('Request must be POST.')


def Messages(request):
    courseId = 0
    if 'course_id' in request.session:
        courseId = request.session['course_id']
    c = Chat.objects.filter(courseid=courseId)
    return render(request, 'messages.html', {'chat': c})
