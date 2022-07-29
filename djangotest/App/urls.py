from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),

#teacher
    url(r'^login_teacher/', views.login_teacher, name='login_teacher'),
    url(r'^register_teacher/', views.register_teacher, name='register_teacher'),
    url(r'^reset_teacher/', views.reset_teacher, name='reset_teacher'),
    url(r'^teacher_home/', views.teacher_home, name='teacher_home'),
    url(r'^logout_teacher/', views.logout_teacher, name='logout_teacher'),
    url(r'^resetteacher/', views.resetteacher, name='resetteacher'),


#student
    url(r'^login_student/', views.login_student, name='login_student'),
    url(r'^student_home/', views.student_home, name='student_home'),
    url(r'^logout_student/', views.logout_student, name='logout_student'),
    url(r'^reset_student/', views.reset_student, name='reset_student'),
    url(r'^resetstudent/', views.resetstudent, name='resetstudent'),

    url(r'^checktid/', views.checktid, name='checktid'),

    url(r'^activate/', views.activate, name='activate'),
    url(r'^reactivate/', views.reactivate, name='reactivate'),


    # url(r'^checktlogint/$', views.checklogint, name='checklogint'),
    # url(r'send_email/', views.send_email, name='send_email'),




]