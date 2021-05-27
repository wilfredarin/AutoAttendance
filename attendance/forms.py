from django import forms
from attendance.models import Student
class RegistrationForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ('roll_no','name','dob','email','department','semester','photo')
