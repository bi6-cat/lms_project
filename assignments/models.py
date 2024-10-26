from django.db import models
from courses.models import Course, Lession
from users.models import Student

# Create your models here.
class Assignment(models.Model):
    lession = models.ForeignKey(Lession, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    objects = models.Manager()
    
    
class SubmitAssignment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment_file = models.FileField(null=True, blank=True,upload_to='uploads/')
    marks = models.IntegerField(default=0)
    content = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# tài liệu cho bài tập
class AssignmentResource(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=50)  # Loại tài nguyên (document, video, link)
    resource_file = models.FileField(upload_to='resources/', null=True, blank=True)  # Trường upload file
    resource_url = models.CharField(max_length=255, null=True, blank=True)  # Đường dẫn tài nguyên (có thể không cần nếu có file)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.resource_url if self.resource_url else str(self.resource_file)

