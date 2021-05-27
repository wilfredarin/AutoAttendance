from django.db import models

# Create your models here.
from django.db import models


SEMESTER_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
)
Department_CHOICES = (
    ("CS", "CS"),
    ("IT", "IT"),
    ("ECE", "ECE"),
    ("EEE", "EEE"),
    ("ME", "ME"),
)

# Create your models here.
class Student(models.Model):
	roll_no = models.IntegerField(primary_key=True)
	name =  models.CharField(max_length=30)
	dob = models.DateField()
	department = models.CharField(
		max_length = 30,
		choices = Department_CHOICES,
		default = 'ECE')
	semester = models.CharField(
		max_length = 30,
		choices = SEMESTER_CHOICES,
		default = '1')
	email = models.EmailField()
	photo = models.ImageField(upload_to='images/')

class AttendanceTable(models.Model):
	date = models.DateField()
	time = models.TimeField()
	student = models.ForeignKey(Student,on_delete=models.CASCADE)