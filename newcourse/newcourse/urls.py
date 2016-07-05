"""newcourse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'app.views.login'),
    url(r'^login/$', 'app.views.login'),
    url(r'^logout/$', 'app.views.logout'),
    url(r'^change_password/$', 'app.views.change_password'),

    url(r'^student/$', 'app.student.student'),
    url(r'^student/info/$', 'app.student.student_info'),
    url(r'^student/course/$', 'app.student.student_course'),
    url(r'^student/group/$', 'app.student.student_group'),
    url(r'^student/course/(\d)+/$','app.student.student_course_i'),
    url(r'^student/course/(\d)+/homework/$','app.student.student_course_i_homework'),


    url(r'^teacher/$', 'app.teacher.teacher_info'),
    url(r'^teacher/info/$','app.teacher.teacher_info'),
    url(r'^teacher/course/$','app.teacher.teacher_course'),
    url(r'^teacher/course/(?P<courseId>\d+)/$','app.teacher_course.course_teacher_info'),
    url(r'^teacher/course/resource/$','app.teacher_course.course_resource'),
    url(r'^teacher/course/resource_publish/$','app.teacher_course.course_resource_publish'),
    url(r'^teacher/course/task/$','app.teacher_course.course_task'),
    url(r'^teacher/course/task_publish/$','app.teacher_course.course_task_publish'),
    url(r'^teacher/course/task_info/(?P<task_id>\d+)/$','app.teacher_course.course_task_info'),
    url(r'^teacher/course/task_grade/$','app.teacher_course.course_task_grade'),
    url(r'^teacher/course/task_comment/$','app.teacher_course.course_task_comment'),

    url(r'^administrator/term/$','app.administrator_term.modifyTerm'),

    url(r'^administrator/$', 'app.administrator.administrator'),
    url(r'^administrator/course/$','app.administrator_course.main'),
    url(r'^administrator/course/courseInfo/(?P<courseId>\d+)/$', 'app.administrator_course.courseInfo'),
    url(r'^administrator/course/changeCourse/(?P<courseId>\d+)/$', 'app.administrator_course.changeCourseShow'),
    url(r'^administrator/course/addCourse/$', 'app.administrator_course.addCourseShow'),
    url(r'^administrator/course/saveCourse/$', 'app.administrator_course.save_course'),
    url(r'^chatpost/','app.course_chat.Post'),
    url(r'^teacher/course/message/','app.course_chat.Home'),
    url(r'^messages/$', 'app.course_chat.Messages', name='messages'),

    url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_URL}),

]
