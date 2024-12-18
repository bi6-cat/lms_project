# Generated by Django 5.0.6 on 2024-10-27 08:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('ongoing', 'Đang học'), ('completed', 'Đã hoàn thành'), ('upcoming', 'Sắp tới')], default='ongoing', max_length=20)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='LessonResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_type', models.CharField(choices=[('document', 'Tài liệu'), ('video', 'Video'), ('slide', 'Bài giảng'), ('audio', 'Audio')], default='document', max_length=50)),
                ('resource_status', models.CharField(choices=[('draft', 'Bản nháp'), ('published', 'Xuất bản')], default='draft', max_length=20)),
                ('resource_file', models.FileField(upload_to='lesson_resources/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='lessons.lesson')),
            ],
        ),
    ]
