
from django import forms
from .models import Assignment, AssignmentResource, SubmitAssignment

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


class AssignmentResourceForm(forms.ModelForm):
    class Meta:
        model = AssignmentResource
        fields = ['resource_type', 'resource_file', 'resource_url']

        widgets = {
            'resource_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Loại tài nguyên'}),
            'resource_file': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'File tài nguyên'}),
            'resource_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Đường dẫn tài nguyên'}),
        }
class AddMarkForm(forms.ModelForm):
    class Meta:
        model = SubmitAssignment
        fields = ['marks']

        widgets = {
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Điểm số'}),
        }


