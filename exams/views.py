import csv
import os
from django.shortcuts import render
from django.db import models

from courses.models import Course
from exams.forms import ExamForm, ExamKeyForm, KeyUpLoadForm
from exams.models import Exam, Examkey
from lms_project import settings
from users.models import Student
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.
# 6. Exams App (Quản lý thi trắc nghiệm)
# /exams/: Danh sách các kỳ thi.
# /exams/add/: Tạo kỳ thi mới (Teacher).
# /exams/<int:exam_id>/edit/: Chỉnh sửa kỳ thi (Teacher).
# /exams/<int:exam_id>/delete/: Xóa kỳ thi (Teacher/Admin).
# /exams/<int:exam_id>/answers/: Xem câu trả lời và điểm của bài thi trắc nghiệm.
# /exams/<int:exam_id>/scan/: Quét bài thi trắc nghiệm để chấm điểm tự động (Teacher).
# /exams/reports/: Xuất báo cáo kết quả thi dưới dạng file CSV hoặc PDF (Teacher/Admin).
class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'teacher'

    def handle_no_permission(self):
        return redirect('home') 
# Tao 1 ky thi
class AddExamView(TeacherRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exams/add_exam.html'
    def get_success_url(self):
        # Lấy course_id từ kwargs
        course_id = self.kwargs.get('course_id')
        # Sử dụng course_id để tạo đường dẫn
        return reverse_lazy('show_exam', args=[course_id])

    def form_valid(self, form):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        form.instance.course = course
        return super().form_valid(form)


def show_exam(request, course_id):
    exams = Exam.objects.filter(course=course_id)
    return render(request, 'exams/show_exam.html', {
        'exams': exams
    })
# Chinh sua ki thi
class EditExamView(TeacherRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exams/edit_exam.html'
    def get_success_url(self):
        # Lấy course_id từ kwargs
        course_id = self.kwargs.get('course_id')
        # Sử dụng course_id để tạo đường dẫn
        return reverse_lazy('show_exam', args=[course_id])
    def form_valid(self, form):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        form.instance.course = course
        return super().form_valid(form)
# Xoa ky thi
class DeleteExamView(TeacherRequiredMixin, DeleteView):
    model = Exam
    template_name = 'exams/delete_exam.html'  #Template xac nhan xoa
    def get_success_url(self):
        # Lấy course_id từ kwargs
        exam = self.get_object()
        course = exam.course
        course_id = course.id
        # Sử dụng course_id để tạo đường dẫn
        return reverse_lazy('show_exam', args=[course_id])
    def test_func(self):
        exam = self.get_object()
        course = exam.course
        teacher = course.teacher
        if self.request.user.role == 'teacher':
            return True
        return False
    
# Tao dap an cho bai thi, tao tung cau 1
class AddExamKeyView(TeacherRequiredMixin, CreateView):
    model = Examkey
    form_class = ExamKeyForm
    template_name = 'exams/add_examkey.html'
    success_url = reverse_lazy('show_exam')
    def form_valid(self, form):
        exam_id = self.kwargs.get('exam_id')
        exam = get_object_or_404(Exam, id=exam_id)
        form.instance.exam = exam
        return super().form_valid(form)
    
# Edit dap an cho bai thi
class EditExamKeyView(TeacherRequiredMixin, UpdateView):
    model = Examkey
    form_class = ExamKeyForm
    template_name = 'exams/edit_examkey.html'
    # success_url = reverse_lazy('show_exam')
    
    def test_func(self):
        examkey = self.get_object()
        if self.request.user.role == 'teacher':
            return True
        return False
    
# Xoa dap an cho bai thi
class DeleteExamKeyView(TeacherRequiredMixin, DeleteView):
    model = Examkey
    template_name = 'exams/delete_examkey.html'
    success_url = reverse_lazy('show_exam')
    
    def test_func(self):
        examkey = self.get_object()
        if self.request.user.role == 'teacher':
            return True
        return False
 
# Ham lay dap an tu file csv
def transform_answer(request, exam_id):
    if(request.method == "POST"):
        exam = Exam.objects.get(id=exam_id)
        course_id = exam.course.id
        form = KeyUpLoadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = request.FILES['file']
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'exam_key')
            path = os.path.join(upload_dir, upload_file.name)  # Sử dụng đường dẫn đã tạo ở trên
            with open(path, 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)
            with open(path ,'r') as f:
                reader = csv.reader(f)
                for  row in reader:
                    question_number = row[0]
                    correct_answer = row[1]
                    examkey = Examkey.objects.create(exam=exam, question_number=question_number, correct_answer=correct_answer)
                    examkey.save()
            message = 'File uploaded successfully'
            # Chua buu show_error.html
            #  Cho nay su dung redict de khi tai lai trang no k tu upload lai file
            return render(request, 'exams/show_error.html', {'message': message})
    return render(request, 'exams/get_examkey.html', {'form': KeyUpLoadForm()})
                