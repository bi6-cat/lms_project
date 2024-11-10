from django.db import models


# lessons/models.py

from django.db import models

class Lesson(models.Model):
    course = models.ForeignKey('courses.Course', related_name='lessons',on_delete=models.CASCADE)
    lesson_title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('ongoing', 'Đang học'),
        ('completed', 'Đã hoàn thành'),
        ('upcoming', 'Sắp tới')
    ]    
    objects = models.Manager()


    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')

    def __str__(self):
        return self.lesson_title

class LessonResource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="resources")
    resource_type = models.CharField(max_length=50, choices=[('document', 'Tài liệu'), ('video', 'Video'), ('slide', 'Bài giảng'), ('audio', 'Audio') ], default='document')
    resource_status = models.CharField(max_length=20, choices=[('draft', 'Bản nháp'), ('published', 'Xuất bản')], default='draft')
    resource_file = models.FileField(upload_to='lesson_resources/')  # Thư mục để lưu file
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.resource_type} - {self.lesson.lesson_title}"
    
