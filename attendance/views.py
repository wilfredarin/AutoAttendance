from django.http import HttpResponse
import cv2 
import numpy as np 
import face_recognition
import datetime
import time
from django.shortcuts import render
from .forms import *
from .models import Student,AttendanceTable
import os

def index(request):
	path="attendance/images"+"college_pic.jpg"
	print(path)
	return render(request,"attendance/index.html",{'path':path})

def registerStudent(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			name = form.cleaned_data['name']
			dob = form.cleaned_data['dob']
			department = form.cleaned_data['department']
			semester = form.cleaned_data['semester']
			roll_no = form.cleaned_data['roll_no']
			email = form.cleaned_data['email']
			photo = form.cleaned_data['photo']
			form.save()	
			students = Student.objects.all()
			records = {}
			for i in range(len(students)):
				t = students[i]
				records[i+1]={'roll':t.roll_no,'name':t.name,'department':t.department,'semester':t.semester}
			return render(request,"attendance/show_student.html",{'context':records})
	else:
		form  = RegistrationForm()
	return render(request, 'attendance/registration.html', {'form' : form})


def markAttendance(request):
	students = Student.objects.all()
	images = []
	imagesNames = []
	imagesRoll = []
	window_width = 450
	window_height = 450
	path = os.getcwd()
	for s in students:
		surl = s.photo.url
		name = s.name
		roll = s.roll_no
		img = cv2.imread(path+"/"+surl)
		images.append(img)
		imagesNames.append(name)
		imagesRoll.append(roll)

	
	def findEncodings(imagesList):
		encodedList  = []
		for img in imagesList:
			img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
			enc = face_recognition.face_encodings(img)[0]
			encodedList.append(enc)
			print("Encoding in progress")
		return encodedList
	encodeListKnown = findEncodings(images)
	cap = cv2.VideoCapture(0)
	Flag = True
	markedFlag = False
	name = None
	while Flag:
		success, img = cap.read()
		#reduce size of image - scale .25,0.25, 1/4th of image
		imgS = cv2.resize(img,(0,0),None,0.25,0.25)
		imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
		cv2.putText(img,"Press ESC to Close",(100,100),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
		#in web cam we can see many faces so find the loc of faces
		facesCurFrame = face_recognition.face_locations(imgS)
		encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)


		for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
			matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
			#faceDis give distance of all the known face from web face
			faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
			print(faceDis)
			#index of min face
			matchIndex = np.argmin(faceDis)
			if matches[matchIndex]:
				name = imagesNames[matchIndex].upper()
				roll= imagesRoll[matchIndex]
				y1,x2,y2,x1 = faceLoc
				y1 *=4
				x1 *=4
				y2 *=4
				x2 *=4
				#scale up face loc
				cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
				cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
				cv2.putText(img,"Mr "+name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
				
				curStudent = Student.objects.get(pk=roll)
				if not AttendanceTable.objects.filter(student__roll_no = roll,date__day=datetime.date.today().day):
					b = AttendanceTable(date =datetime.date.today() ,time=datetime.datetime.now().time(),student=curStudent)
					b.save()
					markedFlag = 1
				if markedFlag:
					cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
					cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
					cv2.putText(img,"Mr "+name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
					cv2.putText(img,"Attendance Marked for Mr "+name,(x1+6,y2-56),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
					Flag = 0
					time.sleep(2)
					cap.release()
					cv2.destroyAllWindows()
					return render(request,"attendance/index.html",{'name':name})
				# cv2.resizeWindow('Resized Window', window_width, window_height)
		cv2.imshow('Webcam',img)
		k = cv2.waitKey(1)
		if k%256 == 27:
			Flag = 0
			cap.release()
			cv2.destroyAllWindows()
			return render(request,"attendance/index.html",{'name':name})


def showStudentList(request):
	students = Student.objects.all()
	records = {}
	for i in range(len(students)):
		t = students[i]
		records[i+1]={'roll':t.roll_no,'name':t.name,'department':t.department,'semester':t.semester}
	return render(request,"attendance/show_student.html",{'context':records})

def getStudentByID(request,id):
	daysAttended = AttendanceTable.objects.filter(student__roll_no = id)
	
	ctx = {
				
			'student': Student.objects.get(pk=id),
		}
	if daysAttended:
		ctx['daysattended'] = len(daysAttended)
	return render(request,"attendance/display_student.html",ctx)

def showAttendanceRecord(request):
	attendance = AttendanceTable.objects.all()
	records = {}
	for rec in range(len(attendance)):
		t = attendance[rec]
		records[rec+1]={'date':t.date,'time':t.time,'roll':t.student.roll_no,'name':t.student.name,'department':t.student.department}
	print(records)
	return render(request,"attendance/attendance_record.html",{"context":records})