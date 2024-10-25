from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

 # UserRegistrationForm, UserLoginForm, UserProfileForm
 
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name' , 'password1', 'password2', 'role']  # Các trường cần điền
        
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']  # Các trường cần chỉnh sửa
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']  # Các trường có thể chỉnh sửa
