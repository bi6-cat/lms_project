from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Teacher, Student

 # UserRegistrationForm, UserLoginForm, UserProfileForm
 
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'role']

        
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['department']
        
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['school_name']