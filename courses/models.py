# courses/models.py

from django.db import models
from users.models import User  # Giả sử User được định nghĩa trong app users

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    start_date = models.DateField()  
    end_date = models.DateField()
    rate = models.FloatField(default=0)
    background = models.ImageField(upload_to='course_backgrounds/')
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

class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="resources")
    resource_type = models.CharField(max_length=50, choices=[('document', 'Document'), ('video', 'Video'), ('link', 'Link')])
    resource_file = models.FileField(upload_to='course_resources/')  # Thư mục để lưu file
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resource_type} - {self.course.title}"