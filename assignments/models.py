from django.db import models
from users.models import Student
from lessons.models import Lesson

# Create your models here.
class Assignment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    objects = models.Manager()
    
    
class SubmitAssignment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment_file = models.FileField(null=True, blank=True,upload_to='uploads/')
    marks = models.IntegerField(null=True, blank=True)
    comment = content = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# tài liệu cho bài tập
class AssignmentResource(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=50, choices=[('document', 'Document'), ('video', 'Video'), ('link', 'Link')])
    resource_file = models.FileField(upload_to='resources/', null=True, blank=True)  # Trường upload file
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.resource_url if self.resource_url else str(self.resource_file)

