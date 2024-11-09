from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from courses.models import Course, Enrollment
from lessons.models import Lesson
from users.models import Student, User
from .models import Assignment, AssignmentResource, SubmitAssignment
from assignments.forms import AddMarkForm, AssignmentForm, SubmitAssignmentForm

# Create your views here.
# Mixin để kiểm tra xem người dùng có phải là giáo viên không
class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'teacher'

    def handle_no_permission(self):
        return redirect('home')  # Chuyển hướng đến trang chủ nếu không đủ quyền



class AssignmentCreateView(TeacherRequiredMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignment/create_assignment.html'
    success_url = reverse_lazy('show_assignment') 
    def form_valid(self, form):
        lesson_id = self.kwargs.get('lesson_id')
        lesson = get_object_or_404(Lesson, id=lesson_id)
        # assignment = form.save(commit=False)
        form.instance.lesson = lesson # 
        return super().form_valid(form)
        # return redirect('show_assignment')
    # def create_success(self):
    #     # Điều hướng đến trang chi tiết của khóa học sau khi cập nhật thành công
    #     return reverse('course_detail', kwargs={'course_id': self.object.id})
    
def show_assignment(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignment/show_assignment.html', {
        'assignments': assignments
    })


def show_error(request):
    return render(request, 'assignment/show_error.html')
class SubmitAssignmentWiew(CreateView):
    model = SubmitAssignment
    form_class = SubmitAssignmentForm
    template_name = 'assignment/submit_assignment.html'
    # Show den cai thong bao nop bai thanh cong
    success_url = reverse_lazy('show_assignment')
   
    def form_valid(self, form):
        if( self.request.user.role == 'teacher'):
            message = 'Teacher can not submit assignment'
            return render(self.request, 'assignment/show_error.html', {'message': message})
        assignment_id = self.kwargs.get('assignment_id')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        student = self.request.user.student
        form.instance.assignment = assignment # 
        form.instance.student = student
        # assignment.save()
        return super().form_valid(form)
    

def show_all_assignment(request, lesson_id):
    assignments = Assignment.objects.filter(lesson=lesson_id)
    return render(request, 'assignment/show_assignment.html', {
        'assignments': assignments
    })

class DeleteAssignmentView(TeacherRequiredMixin,DeleteView):
    model = Assignment
    template_name = 'assignment/delete_assignment.html'
    success_url = reverse_lazy('show_assignment')

    #  ham tést_func() thuong dung cho TeacherRequiredMixin
    def test_func(self):
        assignment = self.get_object()
        lesson = assignment.lesson
        course = lesson.course
        teacher = course.teacher
        #  get_object(): tra ve doi tuong xoa
        assignment = self.get_object() 
        if self.request.user.role == 'teacher':
            # print(teacher)
            # print(self.request.user.teacher)
            return True
        return False  # Chỉ cho phép chủ sở hữu xóa


class UpdateAssignmentView(TeacherRequiredMixin,UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignment/update_assignment.html'
    success_url = reverse_lazy('show_assignment')
    
    def test_func(self):
        assignment = self.get_object()
        if self.request.user.role == 'teacher':
            # print(teacher)
            # print(self.request.user.teacher)
            return True
        return False  # Chỉ cho phép chủ sở hữu xóa


class CreateAssignmentResourceView(TeacherRequiredMixin,CreateView):
    model = AssignmentResource
    form_class = AssignmentForm
    template_name = 'assignment/create_assignment.html'
    success_url = reverse_lazy('show_assignment')
    
    def form_valid(self, form):
        assignment_id = self.kwargs.get('assignment_id')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        form.instance.assignment = assignment
        return super().form_valid(form)

#  Ca thay doi va them diem deu su dung ham nay
class AddMarkView(TeacherRequiredMixin,UpdateView):
    model = SubmitAssignment
    form_class = AddMarkForm
    template_name = 'assignment/add_mark_assignment.html'
    success_url = reverse_lazy('show_assignment')
   
    def test_func(self):
        assignment = self.get_object()
        if self.request.user.role == 'teacher':
            return True
        return False
    

def assignment_submission_status(request, id_assignment):
    # Lấy Assignment theo id
    assignment = get_object_or_404(Assignment, id=id_assignment)
    
    # Lấy khóa học từ bài học
    course = assignment.lesson.course

    # Lấy danh sách học sinh đã đăng ký vào khóa học
    enrollments = Enrollment.objects.filter(course=course)
    students_in_course = [enrollment.student for enrollment in enrollments]

    # Lấy danh sách học sinh đã nộp bài
    students_submitted_ids = SubmitAssignment.objects.filter(assignment=assignment).values_list('student', flat=True)
    
    # Phân loại học sinh đã nộp và chưa nộp
    students_submitted = [student for student in students_in_course if student.id in students_submitted_ids]
    students_not_submitted = [student for student in students_in_course if student.id not in students_submitted_ids]

    return render(request, 'assignment/assignment_submission_status.html', {
        'assignment': assignment,
        'course': course,
        'students_submitted': students_submitted,
        'students_not_submitted': students_not_submitted,
    })


#  Xem phan hoi va diem so cua hoc sinh. Thoi m tu viet di quang a. 
# M chi can viet ham for la ra
# def student_watch_mark(request, id_submitassignment):
#     submit_assignment = get_object_or_404(SubmitAssignment, id=id_submitassignment)
#     if(submit_assignment.marks == None):
        
#     submit_assignments = SubmitAssignment.objects.filter(student=request.user.student)
#     return render(request, 'assignment/show_assignment.html', {
#         'submit_assignments': submit_assignments
#     })


# 5. Assignments App (Quản lý bài tập)
# /assignments/: Danh sách tất cả các bài tập của học sinh.
# /assignments/add/: Tạo bài tập mới (Teacher).
# /assignments/<int:assignment_id>/submit/: Nộp bài tập (Student).
# /assignments/<int:assignment_id>/edit/: Chỉnh sửa bài tập (Teacher).
# /assignments/<int:assignment_id>/delete/: Xóa bài tập (Teacher/Admin).
# /assignments/<int:assignment_id>/grade/: Chấm điểm bài tập (Teacher).
# /assignments/<int:assignment_id>/status/: Xem trạng thái nộp bài (Student/Teacher).
# Ngoài ListView và DetailView, còn có các view khác như CreateView, UpdateView, và DeleteView.





