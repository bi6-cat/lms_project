from exams.Scan_score import *
from exams.Scan_score.test_scanner import Test_Scanner
import csv
import os
import cv2
from django.shortcuts import render
from matplotlib import pyplot as plt
from django.contrib.auth.decorators import login_required
from users.decorators import teacher_required
from courses.models import Course, Enrollment
from exams.Scan_score.test_scanner import Test_Scanner
from exams.forms import ExamForm, ExamKeyForm, KeyUpLoadForm, SubmitAnswerForm
from exams.models import Exam, Examkey, SubmitExam
from lms_project import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import  CreateView, UpdateView, DeleteView

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
        return reverse_lazy('course_detail', args=[course_id])

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
        # Lấy exam_id từ instance
        exam_id = self.object.id
        # Sử dụng exam_id để tạo đường dẫn
        return reverse_lazy('exam_detail', args=[exam_id])

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam_id'] = self.object.id
        return context
    

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
        return reverse_lazy('course_detail', args=[course_id])
    def test_func(self):
        exam = self.get_object()
        course = exam.course
        teacher = course.teacher
        if self.request.user.role == 'teacher':
            return True
        return False

@login_required
@teacher_required
def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    course = exam.course
    
    # Get all enrolled students
    enrollments = Enrollment.objects.filter(course=course)
    students_in_course = [enrollment.student for enrollment in enrollments]
    
    # Get submitted exams
    submitted_exams = SubmitExam.objects.filter(exam=exam)
    submitted_students_ids = submitted_exams.values_list('student', flat=True)
    
    # Split students into submitted and not submitted
    students_submitted = [student for student in students_in_course if student.id in submitted_students_ids]
    students_not_submitted = [student for student in students_in_course if student.id not in submitted_students_ids]
    
    # Get exam keys
    exam_keys = Examkey.objects.filter(exam=exam).order_by('question_number')
    
    # Create dictionary of submissions with scores
    submissions_dict = {
        submission.student.id: submission for submission in submitted_exams
    }

    context = {
        'exam': exam,
        'course': course,
        'students_submitted': students_submitted,
        'students_not_submitted': students_not_submitted,
        'exam_keys': exam_keys,
        'submissions_dict': submissions_dict,
    }
    
    return render(request, 'exams/exam_detail.html', context)
# Edit dap an cho bai thi
class EditExamKeyView(TeacherRequiredMixin, UpdateView):
    model = Examkey
    form_class = ExamKeyForm
    template_name = 'exams/edit_examkey.html'
    
    def test_func(self):
        examkey = self.get_object()
        return self.request.user.role == 'teacher'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam_id'] = self.kwargs.get('exam_id')
        return context
    
    def get_success_url(self):
        exam_id = self.kwargs.get('exam_id')
        return reverse_lazy('exam_detail', kwargs={'exam_id': exam_id})
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

# Xoa tat ca dap an cua bai thi
@login_required
@teacher_required
def delete_all_exam_keys(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        Examkey.objects.filter(exam=exam).delete()
        return redirect('show_exam', course_id=exam.course.id)
    return render(request, 'exams/delete_all_exam_keys.html', {'exam': exam})
 
# Ham lay dap an tu file csv
from django.shortcuts import redirect
from django.urls import reverse

def get_key(request, exam_id):
    if request.method == "POST":
        exam = Exam.objects.get(id=exam_id)
        form = KeyUpLoadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = request.FILES['file']
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'exam_key')
            path = os.path.join(upload_dir, upload_file.name)
            with open(path, 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)
            with open(path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    question_number = row[0]
                    correct_answer = row[1]
                    Examkey.objects.create(exam=exam, question_number=question_number, correct_answer=correct_answer)
            # Chuyển hướng về trang chi tiết
            return redirect(reverse('exam_detail', args=[exam_id]))
    return render(request, 'exams/get_examkey.html', {'form': KeyUpLoadForm()})


# Ham nop bai tu hoc sinh
class SubmitAnswerView(CreateView):
    model = SubmitExam
    form_class = SubmitAnswerForm
    template_name = 'exams/submit_answer.html'
    success_url = reverse_lazy('show_exam')
    def form_valid(self, form):
        exam_id = self.kwargs.get('exam_id')
        exam = get_object_or_404(Exam, id=exam_id)
        student = self.request.user.student
        form.instance.exam = exam
        form.instance.student = student
        return super().form_valid(form)
    
    
def get_files_inTestPics():
    return [x for x in os.listdir('D:/Code/Python/Project_Python/lms_project/media/uploads_key_student/images')] #Duong dan tuyet doi ta co the thay bang duong dan tuong doi

def cham_tat_ca(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    submits = SubmitExam.objects.filter(exam=exam)
    results = []
    for submit in submits:
        examfile = submit.exam_file
        path = os.path.join(settings.MEDIA_ROOT, examfile.name)
        answer = ['A'] * 50
        widthImg = 800
        heightImg = 800
        img = cv2.imread(path)
        img = cv2.resize(img, (widthImg, heightImg))
        T_scanner = Test_Scanner(answer, img)
        id_student, score, id_exam = T_scanner.get_Infor()
        submit.marks = score
        submit.save()
        results.append({
            'id_student': id_student,
            'score': score,
            'id_exam': id_exam,
        })
    return render(request, 'exams/cham_bai.html', { 'results': results })
        

                