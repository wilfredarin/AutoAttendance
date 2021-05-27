from django.shortcuts import render

# Create your views here.
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/',views.registerStudent, name='register'),
    path('markattendance/',views.markAttendance, name='markattendance'),
    path('showstudentlist/',views.showStudentList, name='showstudentlist'),
    path('attendancerecord/',views.showAttendanceRecord, name='attendancerecord'),
    path('<int:id>/', views.getStudentByID, name='getstudentbyid')
]

