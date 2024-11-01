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
        lession_id = self.kwargs.get('lession_id')
        lession = get_object_or_404(Lesson, id=lession_id)
        # assignment = form.save(commit=False)
        form.instance.lession = lession # 
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

# 5. Assignments App (Quản lý bài tập)
# /assignments/: Danh sách tất cả các bài tập của học sinh.
# /assignments/add/: Tạo bài tập mới (Teacher).
# /assignments/<int:assignment_id>/submit/: Nộp bài tập (Student).
# /assignments/<int:assignment_id>/edit/: Chỉnh sửa bài tập (Teacher).
# /assignments/<int:assignment_id>/delete/: Xóa bài tập (Teacher/Admin).
# /assignments/<int:assignment_id>/grade/: Chấm điểm bài tập (Teacher).
# /assignments/<int:assignment_id>/feedback/: Xem phản hồi và điểm số từ Teacher (Student).
# /assignments/<int:assignment_id>/status/: Xem trạng thái nộp bài (Student/Teacher).
# Ngoài ListView và DetailView, còn có các view khác như CreateView, UpdateView, và DeleteView.

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
    

def show_all_assignment(request, lession_id):
    assignments = Assignment.objects.filter(lession=lession_id)
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
        lession = assignment.lession
        course = lession.course
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

#  Xem phan hoi va diem so cua hoc sinh. Thoi m tu viet di quang a. 
# M chi can viet ham for la ra
# def student_watch_mark(request, id_submitassignment):
#     submit_assignment = get_object_or_404(SubmitAssignment, id=id_submitassignment)
#     if(submit_assignment.marks == None):
        
#     submit_assignments = SubmitAssignment.objects.filter(student=request.user.student)
#     return render(request, 'assignment/show_assignment.html', {
#         'submit_assignments': submit_assignments
#     })


# Danh sach cac hoc sinh chua nop bai
def student_not_submit(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    students = Student.objects.all()
    submit_assignments = SubmitAssignment.objects.filter(assignment=assignment)
    return render(request, 'assignment/student_not_submit.html', {
        'students': students,
        'submit_assignments': submit_assignments
    })

# Trang thai nop bai cua hoc sinh
def show_status_submit(request, id_submit_assignment):

    submit_assignment = get_object_or_404(SubmitAssignment, id=id_submit_assignment)
    message = 'Da nop bai'
    if(submit_assignment.content == None or submit_assignment.assignment_file == None):
        message = 'Chua nop bai'
    return render(request, 'assignment/show_status_submit.html', {
        'message': message
    })

# In ra danh sach hoc sinh chua nop bai

def student_not_submit(request, id_assignment):
    assignment = get_object_or_404(Assignment, id=id_assignment)
    course = assignment.lession.course
    enrollments = Enrollment.objects.filter(course=course)
    # students = [enrollment.student for enrollment in enrollments]
    submit_assignments = SubmitAssignment.objects.filter(assignment=assignment)
    student_submitted = []
    for x in submit_assignments:
        stu = Student.objects.get(id=x.student.user.id)
        print(stu.user.email)
        student_submitted.append(stu.user.email)
    student_not_submit = []
    for x in enrollments:
        stu = Student.objects.get(id=x.student.user.id)
        # print(stu.email)
        if stu.user.email not in student_submitted:
            student_not_submit.append(stu.user)
    return render(request, 'assignment/student_not_submit.html', {
        'students': student_not_submit,
    })

    














