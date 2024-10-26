# courses/models.py

from django.db import models
from users.models import User  # Giả sử User được định nghĩa trong app users

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    start_date = models.DateField()  # Thêm trường này
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} enrolled in {self.course} at {self.enrolled_at}"

class Lession(models.Model):    
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    lession_name = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    creater_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
class LessionResource(models.Model):
    id = models.AutoField(primary_key=True)
    lession_id = models.ForeignKey(Lession, on_delete=models.CASCADE)
    resource_name = models.CharField(max_length=255)
    resource_content = models.FileField(upload_to='uploads/')
    creater_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()