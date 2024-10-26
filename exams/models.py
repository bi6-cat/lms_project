from django.db import models
from courses.models import Course
from users.models import Student
# Create your models here.
class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    creater_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

