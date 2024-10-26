from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from courses.models import Course
from .models import Assignment
from assignments.forms import AssignmentForm, SubmitAssignmentForm

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
        lession = get_object_or_404(Course, id=lession_id)
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

class SubmitAssignmentWiew(CreateView):
    model = Assignment
    form_class = SubmitAssignmentForm
    template_name = 'assignment/submit_assignment.html'
    # Show den cai thong bao nop bai thanh cong
    # success_url = reverse_lazy('show_assignment')
    def form_valid(self, form):
        assignment_id = self.kwargs.get('assignment_id')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        student = self.request.user
        form.instance.assignment = assignment # 
        form.instance.student = student
        # assignment.save()
        return super().form_valid(form)










    