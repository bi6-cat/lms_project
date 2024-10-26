
from django import forms
from .models import Assignment, SubmitAssignment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description','due_date']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề bài tập'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Mô tả bài tập'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Ngày hết hạn'}),

        }

class SubmitAssignmentForm(forms.ModelForm):
    class Meta:
        model = SubmitAssignment
        fields = ['assignment_file', 'content']

        widgets = {
            'assignment_file': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'File bài tập'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nội dung bài tập'}),
        }



