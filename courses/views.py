from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from exams.models import Exam, SubmitExam
from lessons.models import Lesson
from users.models import Student, User
from .models import Course, Enrollment
from .forms import CourseForm  
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Mixin để kiểm tra xem người dùng có phải là giáo viên không
class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'teacher'

    def handle_no_permission(self):
        return redirect('403')  # Chuyển hướng đến trang chủ nếu không đủ quyền



@login_required
def course_list(request):
    courses = Course.objects.all()
    enrolled_courses = Enrollment.objects.filter(student=request.user).values_list('course', flat=True)
    
    # Tạo dictionary chứa số lượng học sinh cho mỗi khóa học
    course_student_counts = {}
    for course in courses:
        course_student_counts[course.id] = Enrollment.objects.filter(course=course).count()

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses,
        'course_student_counts': course_student_counts,
    })


# courses/views.py

class CourseCreateView(TeacherRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/add_course.html'
    
    def form_valid(self, form):
        course = form.save(commit=False)
        course.teacher = self.request.user
        
        if 'background' in self.request.FILES:
            course.background = self.request.FILES['background']
            
        course.save()
        return redirect('course_list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CourseUpdateView(TeacherRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/edit_course.html'
    
    def form_valid(self, form):
        course = form.save(commit=False)
        if 'background' in self.request.FILES:
            course.background = self.request.FILES['background']
        course.save()
        return redirect('course_detail', course_id=course.id)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('course_detail', kwargs={'course_id': self.object.id})
    
# Delete view cho xóa khóa học
class CourseDeleteView(TeacherRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/delete_course.html' # Template xác nhận xóa khóa học
    success_url = '/courses/'  # Chuyển hướng đến danh sách khóa học sau khi xóa


# View để đăng ký khóa học
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(course=course, student=request.user)
    return redirect('course_detail', course_id=course.id)  # Sử dụng course_id thay vì pk


# View để hủy đăng ký khóa học
@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.filter(course=course, student=request.user).delete()
    return redirect('course_detail', course_id=course.id)  # Sử dụng course_id thay vì pk


# View để tìm kiếm khóa học
@login_required
def search_courses(request):
    query = request.GET.get('q', '') # Lấy từ khóa tìm kiếm từ query string
    courses = Course.objects.filter(title__icontains=query) # Lọc khóa học theo từ khóa tìm kiếm
    return render(request, 'courses/course_list.html', {'courses': courses}) # Trả về trang danh sách khóa học với danh sách khóa học đã lọc



@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)
    exams = Exam.objects.filter(course=course)
    total_students = Enrollment.objects.filter(course=course).count()
    is_enrolled = Enrollment.objects.filter(course=course, student=request.user).exists()

    # Trạng thái bài học
    lessons_status = {}
    if request.user.role == 'student':
        try:
            enrollment = Enrollment.objects.get(course=course, student=request.user)
            for lesson in lessons:
                lessons_status[lesson.id] = {
                    'status': lesson.status,
                    'enrolled_at': enrollment.enrolled_at,
                }
        except Enrollment.DoesNotExist:
            for lesson in lessons:
                lessons_status[lesson.id] = {
                    'status': 'not enrolled',
                    'enrolled_at': None,
                }

    # Trạng thái bài kiểm tra và nộp bài
    exams_status = {}
    submitted_exams = {}
    if request.user.role == 'student':
        student = Student.objects.get(user=request.user)
        for exam in exams:
            exam_result = exam.examresult_set.filter(student=student).first()
            # Kiểm tra xem học sinh đã nộp bài chưa
            submitted = SubmitExam.objects.filter(exam=exam, student=student).exists()
            
            exams_status[exam.id] = {
                'status': 'completed' if exam_result else 'pending',
                'score': exam_result.total_score if exam_result else None,
                'attempt_count': exam.examresult_set.filter(student=student).count(),
                'last_attempt': exam_result.graded_at if exam_result else None,
                'submitted': submitted
            }
            submitted_exams[exam.id] = submitted
            
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'exams': exams,
        'is_enrolled': is_enrolled,
        'lessons_status': lessons_status,
        'exams_status': exams_status,
        'total_students': total_students,
        'submitted_exams': submitted_exams,
    })
    
@login_required
def enrolled_students_list(request, course_id):
    # Lấy khóa học dựa trên course_id
    course = get_object_or_404(Course, id=course_id)
    
    # Lấy danh sách học sinh đã đăng ký khóa học
    enrolled_students = User.objects.filter(enrollment__course=course, role='student')

    return render(request, 'courses/enrolled_students_list.html', {
        'course': course,
        'enrolled_students': enrolled_students,
    })