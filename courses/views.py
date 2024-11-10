from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from lessons.models import Lesson
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


# Create view cho thêm khóa học
class CourseCreateView(TeacherRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/add_course.html'
    
    def form_valid(self, form):
        course = form.save(commit=False) # Lưu form nhưng chưa commit vào database
        form.instance.teacher = self.request.user  # Gán giáo viên cho khóa học
        # course.teacher = self.request.user  # Gán giáo viên cho khóa học
        course.save() # Lưu khóa học
        return redirect('course_list')


# Update view cho chỉnh sửa khóa học
class CourseUpdateView(TeacherRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/edit_course.html'
    
    def get_success_url(self):
        # Điều hướng đến trang chi tiết của khóa học sau khi cập nhật thành công
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

    # Lấy tổng số học sinh tham gia khóa học
    total_students = Enrollment.objects.filter(course=course).count()
    is_enrolled = Enrollment.objects.filter(course=course, student=request.user).exists()

    # Nếu là sinh viên, lấy trạng thái của từng bài học
    lessons_status = {}
    if request.user.role == 'student':
        for lesson in lessons:
            try:
                enrollment = Enrollment.objects.get(course=course, student=request.user)
                lessons_status[lesson.id] = {
                    'status': lesson.status,
                    'enrolled_at': enrollment.enrolled_at,
                }
            except Enrollment.DoesNotExist:
                lessons_status[lesson.id] = {
                    'status': 'not enrolled',
                    'enrolled_at': None,
                }
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'lessons_status': lessons_status,
        'total_students': total_students,
    })