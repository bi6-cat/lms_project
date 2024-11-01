from django.db import models

from courses.models import Course
from users.models import Student
# CREATE TABLE Exam (
#     exam_id INT PRIMARY KEY AUTO_INCREMENT,
#     course_id INT NOT NULL,
#     exam_name VARCHAR(255) NOT NULL,
#     exam_date DATE
# );

# -- Bảng đáp án chuẩn của bài thi
# CREATE TABLE ExamKey (
#     examkey_id INT PRIMARY KEY AUTO_INCREMENT,
#     exam_id INT NOT NULL,
#     question_number INT NOT NULL,
#     correct_answer ENUM('A', 'B', 'C', 'D') NOT NULL,
#     UNIQUE (exam_id, question_number)
# );

# -- Bảng lưu câu trả lời của học sinh cho bài thi
# CREATE TABLE ExamAnswer (
#     answer_id INT PRIMARY KEY AUTO_INCREMENT,
#     exam_id INT NOT NULL,
#     student_id INT NOT NULL,
#     question_number INT NOT NULL,
#     answer ENUM('A', 'B', 'C', 'D') NOT NULL,
#     UNIQUE (exam_id, student_id, question_number)
# );

# -- Bảng lưu kết quả bài thi của học sinh
# CREATE TABLE ExamResult (
#     result_id INT PRIMARY KEY AUTO_INCREMENT,
#     exam_id INT NOT NULL,
#     student_id INT NOT NULL,
#     total_score DECIMAL(5, 2),
#     graded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     UNIQUE (exam_id, student_id)
# );



class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=255)
    exam_date = models.DateField()
    objects = models.Manager

    
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

class Examanswer(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question_number = models.IntegerField()
    answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    objects = models.Manager()
    





