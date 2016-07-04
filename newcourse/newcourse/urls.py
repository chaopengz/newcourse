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
    url(r'^student/$', 'app.student.student'),
    url(r'^teacher/$', 'app.teacher.teacher'),
    url(r'^administrator/$', 'app.administrator.administrator'),
    url(r'^student/info/$', 'app.student.student_info'),
    url(r'^student/course/$', 'app.student.student_course'),
    url(r'^student/group/$', 'app.student.student_group'),
    url(r'^teacher/myinfo/$','app.teacher.teacher_info'),
    url(r'^teacher/mycourse/$','app.teacher.teacher_course'),
    url(r'^jiaowu/term/$','app.jiaowu.modifyTerm'),

    url(r'^course/$', 'app.course.main'),
    url(r'^course/courseInfo/(.+)/$', 'app.course.courseInfo'),

    url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_URL}),
]
