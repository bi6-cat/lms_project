from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course  # Sử dụng model Course
        fields = ['title', 'description', 'start_date', 'end_date']  # Các trường cần có trong form

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề khóa học'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Mô tả khóa học'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
