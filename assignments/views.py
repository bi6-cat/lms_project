from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from courses.models import Course, Enrollment
from lessons.models import Lesson
from users.models import Student, User
from .models import Assignment, AssignmentResource, SubmitAssignment
from assignments.forms import AddMarkForm, AssignmentWithResourceForm, SubmitAssignmentForm

# Create your views here.
# Mixin để kiểm tra xem người dùng có phải là giáo viên không
class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'teacher'

    def handle_no_permission(self):
        return redirect('home')  # Chuyển hướng đến trang chủ nếu không đủ quyền

 
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


class DeleteAssignmentView(TeacherRequiredMixin, DeleteView):
    model = Assignment
    template_name = 'assignment/delete_assignment.html'  # Template xác nhận xóa bài tập
    
    def test_func(self):
        assignment = self.get_object()
        return self.request.user.role == 'teacher'
    
    def get_success_url(self):
        lesson = self.object.lesson
        return reverse('lesson_detail', kwargs={
            'course_id': lesson.course.id,
            'lesson_id': lesson.id
        })


#  Ca thay doi va them diem deu su dung ham nay
class GradeAssignmentView(TeacherRequiredMixin, UpdateView):
    model = SubmitAssignment
    form_class = AddMarkForm
    template_name = 'assignment/grade_assignment.html'
    success_url = reverse_lazy('show_assignment')
   
    def test_func(self):
        return self.request.user.role == 'teacher'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submitted_assignment = self.get_object()
        context['submitted_assignment'] = submitted_assignment
        context['assignment'] = submitted_assignment.assignment
        return context
    
    def get_success_url(self):
        return reverse('assignment_submission_status', kwargs={'id_assignment': self.object.assignment.id})

def assignment_submission_status(request, id_assignment):
    assignment = get_object_or_404(Assignment, id=id_assignment)
    course = assignment.lesson.course
    enrollments = Enrollment.objects.filter(course=course)
    students_in_course = [enrollment.student for enrollment in enrollments]
    
    submit_assignments = SubmitAssignment.objects.filter(assignment=assignment)
    students_submitted_ids = submit_assignments.values_list('student', flat=True)
    
    students_submitted = [student for student in students_in_course if student.id in students_submitted_ids]
    students_not_submitted = [student for student in students_in_course if student.id not in students_submitted_ids]
    
    submitted_assignments_dict = {}
    for submit_assignment in submit_assignments:
        submitted_assignments_dict[submit_assignment.student.id] = {
            'id': submit_assignment.id,
            'submission': submit_assignment
        }
    return render(request, 'assignment/assignment_submission_status.html', {
        'assignment': assignment,
        'course': course,
        'submit_assignments':submit_assignments,
        'students_submitted': students_submitted,
        'students_not_submitted': students_not_submitted,
        'submitted_assignments_dict': submitted_assignments_dict,
    })

class AssignmentCreateView(TeacherRequiredMixin, CreateView):
    model = Assignment
    form_class = AssignmentWithResourceForm
    template_name = 'assignment/create_assignment.html'

    def form_valid(self, form):
        # Lấy lesson dựa vào lesson_id trong URL
        lesson_id = self.kwargs.get('lesson_id')
        lesson = get_object_or_404(Lesson, id=lesson_id)
        
        # Lưu assignment với lesson tương ứng
        form.instance.lesson = lesson
        assignment = form.save()
        
        # Tạo AssignmentResource nếu có resource_file
        if form.cleaned_data.get('resource_file'):
            AssignmentResource.objects.create(
                assignment=assignment,
                resource_file=form.cleaned_data.get('resource_file'),
                resource_type=form.cleaned_data.get('resource_type')
            )
        
        return super().form_valid(form)

    def get_success_url(self):
        # Lấy course_id từ lesson và lesson_id từ URL
        lesson_id = self.kwargs.get('lesson_id')
        lesson = get_object_or_404(Lesson, id=lesson_id)
        course_id = lesson.course.id  # Giả sử mỗi lesson thuộc về một course

        # Tạo URL thành công cho lesson_detail với course_id và lesson_id
        return reverse('lesson_detail', kwargs={'course_id': course_id, 'lesson_id': lesson_id})
    
    
class AssignmentUpdateView(TeacherRequiredMixin, UpdateView):
    model = Assignment
    form_class = AssignmentWithResourceForm
    template_name = 'assignment/update_assignment.html'
    success_url = reverse_lazy('show_assignment')

    def form_valid(self, form):
        assignment = form.save()
        
        # Update or create resource
        resource = assignment.assignmentresource_set.first()
        if form.cleaned_data.get('resource_file') :
            if resource:
                # Update existing resource
                resource.resource_file = form.cleaned_data.get('resource_file') or resource.resource_file
                resource.resource_type = form.cleaned_data.get('resource_type')
                resource.save()
            else:
                # Create new resource
                AssignmentResource.objects.create(
                    assignment=assignment,
                    resource_file=form.cleaned_data.get('resource_file'),
                    resource_type=form.cleaned_data.get('resource_type')
                )
        
        return super().form_valid(form)
