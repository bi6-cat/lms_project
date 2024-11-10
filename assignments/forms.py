
from django import forms
from .models import Assignment, AssignmentResource, SubmitAssignment

class SubmitAssignmentForm(forms.ModelForm):
    class Meta:
        model = SubmitAssignment
        fields = ['assignment_file', 'content']

        widgets = {
            'assignment_file': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'File bài tập'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nội dung bài tập'}),
        }


class AddMarkForm(forms.ModelForm):
    class Meta:
        model = SubmitAssignment
        fields = ['marks', 'comment']

        widgets = {
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Điểm số'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nhận xét của giáo viên'}),
        }

class AssignmentWithResourceForm(forms.ModelForm):
    resource_file = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    resource_type = forms.ChoiceField(
        choices=[('document', 'Document'), ('video', 'Video'), ('audio', 'Audio')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
