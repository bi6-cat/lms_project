from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Thêm các trường tùy chỉnh nếu cần
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)