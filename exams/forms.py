from django import forms

from exams.models import Exam, Examkey, SubmitExam

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_name', 'exam_date']
        widgets = {
            'exam_name': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'type': 'date'})
        }

class ExamKeyForm(forms.ModelForm):
    class Meta:
        model = Examkey
        fields = ['question_number', 'correct_answer']
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'correct_answer': forms.Select(attrs={'class': 'form-control', 'placeholder' :'A B C D'}, )
        }


class KeyUpLoadForm(forms.Form):
    file = forms.FileField(label='Chọn file đáp án', widget=forms.FileInput(attrs={'class': 'form-control'}))

class SubmitAnswerForm(forms.ModelForm):
    class Meta:
        model = SubmitExam
        fields = ['exam_file']
        widgets = {
            'exam_file': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'File đáp án'})
        }

