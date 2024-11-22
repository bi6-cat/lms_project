from django.db import models

from courses.models import Course
from users.models import Student
class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=255)
    exam_description = models.TextField()
    exam_date = models.DateField()
    exam_time = models.TimeField()
    objects = models.Manager()

    
class Examresult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_score = models.DecimalField(max_digits=5, decimal_places=2)
    graded_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Examkey(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_number = models.IntegerField()
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    objects = models.Manager()

class SubmitExam(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_file = models.FileField(null=True, blank=True,upload_to='uploads_key_student/')
    marks = models.FloatField(null=True, blank=True)  
    create_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()




