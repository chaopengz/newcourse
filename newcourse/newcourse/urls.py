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
from django.conf.urls import url, include
from django.contrib import admin
import settings

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^$', 'app.views.login'),
    url(r'^login/$', 'app.views.login'),
    url(r'^logout/$', 'app.views.logout'),
    url(r'^userinfo/$', 'app.views.userinfo'),
    url(r'^save_info/$', 'app.views.save_info'),
    url(r'^info/$', 'app.views.info'),
    url(r'^change_password/$', 'app.views.change_password'),

    url(r'^student/$', 'app.student.student'),
    url(r'^student/info/$', 'app.student.student_info'),
    url(r'^student/course/$', 'app.student.student_course'),
    url(r'^student/group/$', 'app.student.student_group'),
    url(r'^student/course/(\d+)/$','app.student.student_course_i'),
    url(r'^student/course/(\d+)/homework/$','app.student.student_course_i_homework'),
    url(r'^student/course/(\d+)/homework/(\d+)/$','app.student.student_course_i_homework_I'),
    url(r'^student/course/(\d+)/homework/(\d+)/upload/$','app.student.student_course_i_homework_I_upload'),
    # url(r'^student/course/(\d+)/homework/(\d+)/content/$','app.student.student_course_i_homework_I_content'),
    url(r'^student/course/(\d+)/resource/$','app.student.student_course_i_resource'),
    url(r'^student/course/(\d+)/resource/(\d+)/download$','app.student.file_download'),


    # Follow urls are added by chaopengz
    url(r'^student/group/addGroup/$', 'app.student_group.addGroup'),
    url(r'^student/mygroup/$', 'app.student_group.myGroup'),
    url(r'^student/group/join/$', 'app.student_group.join'),
    url(r'^student/group/groupInfo/(\d+)$', 'app.student_group.info'),

    url(r'^teacher/$', 'app.teacher.teacher_info'),
    url(r'^teacher/info/$', 'app.teacher.teacher_info'),
    url(r'^teacher/course/$', 'app.teacher.teacher_course'),
    url(r'^teacher/course/(?P<courseId>\d+)/$', 'app.teacher_course.course_teacher_info'),
    url(r'^teacher/course/resource/$', 'app.teacher_course.course_resource'),
    url(r'^teacher/course/resource_class/$', 'app.teacher_course.course_resource_class'),
    url(r'^teacher/course/resource_class_add/$', 'app.teacher_course.course_resource_class_add'),
    url(r'^teacher/course/resource_publish/$', 'app.teacher_course.course_resource_publish'),
    url(r'^teacher/course/task/$', 'app.teacher_course.course_task'),
    url(r'^teacher/course/task_publish/$', 'app.teacher_course.course_task_publish'),
    url(r'^teacher/course/task_info/(?P<task_id>\d+)/$', 'app.teacher_course.course_task_info'),
    url(r'^teacher/course/task_grade/$', 'app.teacher_course.course_task_grade'),
    url(r'^teacher/course/task_comment/$', 'app.teacher_course.course_task_comment'),
    url(r'^teacher/course/task_content/$', 'app.teacher_course.course_task_content'),
    url(r'^media/(?P<filename>.*)$', 'app.teacher_course.file_download'),
    url(r'^one_click_download/$', 'app.teacher_course.one_click_download'),

    url(r'^administrator/term/$', 'app.administrator_term.main'),
    url(r'^administrator/term/termInfo/(?P<termId>\d+)/$', 'app.administrator_term.termInfo'),
    url(r'^administrator/term/changeTerm/(?P<termId>\d+)/$', 'app.administrator_term.changeTermShow'),
    url(r'^administrator/term/addTerm/$', 'app.administrator_term.modifyTerm'),
    url(r'^administrator/term/saveTerm/$', 'app.administrator_term.save_term'),

    url(r'^administrator/$', 'app.administrator.administrator'),
    url(r'^administrator/course/$', 'app.administrator_course.main'),
    url(r'^administrator/course/courseInfo/(?P<courseId>\d+)/$', 'app.administrator_course.courseInfo'),
    url(r'^administrator/course/changeCourse/(?P<courseId>\d+)/$', 'app.administrator_course.changeCourseShow'),
    url(r'^administrator/course/addCourse/$', 'app.administrator_course.addCourseShow'),
    url(r'^administrator/course/saveCourse/$', 'app.administrator_course.save_course'),
    url(r'^administrator/course/student/$', 'app.administrator_course.student'),
    url(r'^administrator/course/add_student/$', 'app.administrator_course.add_student'),
    url(r'^administrator/course/remove_student/$', 'app.administrator_course.remove_student'),
    url(r'^administrator/teacher/$', 'app.administrator_teacher.main'),
    url(r'^administrator/teacher/reset_password/(?P<tId>\d+)/$', 'app.administrator_teacher.reset_password'),
    url(r'^administrator/teacher/add_teacher/$', 'app.administrator_teacher.add_teacher'),
    url(r'^administrator/teacher/add_teacher_many/$', 'app.administrator_teacher.add_teacher_many'),
    url(r'^administrator/teacher/save_teacher/$', 'app.administrator_teacher.save_teacher'),
    url(r'^administrator/student/$', 'app.administrator_student.main'),
    url(r'^administrator/student/reset_password/(?P<tId>\d+)/$', 'app.administrator_student.reset_password'),
    url(r'^administrator/student/add_student/$', 'app.administrator_student.add_student'),
    url(r'^administrator/student/add_student_many/$', 'app.administrator_student.add_student_many'),
    url(r'^administrator/student/save_student/$', 'app.administrator_student.save_student'),
    url(r'^chatpost/', 'app.course_chat.Post'),
    url(r'^teacher/course/message/', 'app.course_chat.t_Home'),
    url(r'^student/course/(\d+)/message/', 'app.course_chat.s_Home'),
    url(r'^messages/$', 'app.course_chat.Messages', name='messages'),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),

]
