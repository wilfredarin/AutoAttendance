from django.contrib import admin

# Register your models here.
from .models import Student,AttendanceTable

admin.site.register(Student)
admin.site.register(AttendanceTable)