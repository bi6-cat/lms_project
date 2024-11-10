from django import forms
from .models import Lesson, LessonResource

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['lesson_title', 'content', 'status']
        widgets = {
            'lesson_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề bài học'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nội dung bài học'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class LessonResourceForm(forms.ModelForm):
    class Meta:
        model = LessonResource
        fields = ['resource_type', 'resource_status', 'resource_file']
        widgets = {
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'resource_status': forms.Select(attrs={'class': 'form-control'}),
            'resource_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ResourceForm(forms.ModelForm):
    class Meta:
        model = LessonResource
        fields = ['resource_type', 'resource_file']
        widgets = {
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'resource_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
