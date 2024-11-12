from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from assignments.models import Assignment, AssignmentResource, SubmitAssignment
from courses.models import Course, Enrollment
from users.decorators import teacher_required
from users.models import Student
from .models import Lesson, LessonResource
from .forms import LessonForm, LessonResourceForm, ResourceForm

# Hiển thị danh sách bài học trong khóa học
@login_required
def lesson_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)
    
    # Lấy tổng số học sinh tham gia khóa học
    total_students = Enrollment.objects.filter(course=course).count()
    
    # Nếu là sinh viên, lấy trạng thái của từng bài học
    if request.user.role == 'student':
        lessons_status = {}
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
    else:
        lessons_status = {}

    return render(request, 'lessons/lesson_list.html', {
        'course': course,
        'lessons': lessons,
        'lessons_status': lessons_status,
        'total_students': total_students,
    })
    
    
# Hiển thị chi tiết bài học
@login_required
def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    materials = LessonResource.objects.filter(lesson=lesson)
    assignments = Assignment.objects.filter(lesson=lesson)
    assignmentResources = AssignmentResource.objects.filter(assignment__in=assignments)
    
    # Get submission status for each assignment
    submission_status = {}
    if request.user.role == 'student':
        student = Student.objects.filter(user=request.user).first()
        if student:
            for assignment in assignments:
                has_submitted = SubmitAssignment.objects.filter(
                    assignment=assignment,
                    student=student
                ).exists()
                submission_status[assignment.id] = has_submitted

    return render(request, 'lessons/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'materials': materials,
        'assignments': assignments,
        'submission_status': submission_status,
        'assignmentResources': assignmentResources,
    })

@login_required
@teacher_required
def add_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        lesson_form = LessonForm(request.POST)
        resource_form = ResourceForm(request.POST, request.FILES)

        if lesson_form.is_valid():
            # Lưu dữ liệu bài học
            lesson = lesson_form.save(commit=False)
            lesson.course = course
            lesson.save()

            # Kiểm tra tính hợp lệ của resource_form trước khi truy cập cleaned_data
            if resource_form.is_valid() and 'resource_file' in request.FILES:
                resource_type = resource_form.cleaned_data.get('resource_type')
                resource_file = request.FILES['resource_file']
                
                # Lưu LessonResource nếu có file
                resource = LessonResource(
                    lesson=lesson,
                    resource_type=resource_type,
                    resource_file=resource_file,
                )
                resource.save()

            messages.success(request, 'Bài học đã được thêm thành công!')
            return redirect('course_detail', course_id=course.id)
        else:
            messages.error(request, 'Đã xảy ra lỗi. Vui lòng kiểm tra lại thông tin.')
    
    else:
        lesson_form = LessonForm()
        resource_form = ResourceForm()

    context = {
        'lesson_form': lesson_form,
        'resource_form': resource_form,
        'course': course,
    }
    return render(request, 'lessons/add_lesson.html', context)


@login_required
@teacher_required
def edit_lesson(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    if request.method == 'POST':
        lesson_form = LessonForm(request.POST, instance=lesson)
        resource_form = ResourceForm(request.POST, request.FILES)

        forms_valid = True

        if not lesson_form.is_valid():
            forms_valid = False
            messages.error(request, 'Vui lòng kiểm tra lại thông tin bài học.')

        if 'resource_file' in request.FILES and not resource_form.is_valid():
            forms_valid = False
            messages.error(request, 'Vui lòng kiểm tra lại thông tin tài nguyên.')

        if forms_valid:
            lesson = lesson_form.save(commit=False)
            lesson.course = course
            lesson.save()

            if 'resource_file' in request.FILES:
                resource = LessonResource(
                    lesson=lesson,
                    resource_type=resource_form.cleaned_data['resource_type'],
                    resource_file=request.FILES['resource_file'],
                )
                resource.save()

            messages.success(request, 'Bài học đã được chỉnh sửa thành công!')
            return redirect('course_detail', course.id)
    else:
        lesson_form = LessonForm(instance=lesson)
        resource_form = ResourceForm()

    context = {
        'lesson_form': lesson_form,
        'resource_form': resource_form,
        'course': course,
        'lesson': lesson,
    }

    return render(request, 'lessons/edit_lesson.html', context)

# Xóa bài học
@login_required
@teacher_required
def delete_lesson(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    if request.method == 'POST':
        lesson.delete()
        return redirect(reverse('course_detail', args=[course.id]))
    return render(request, 'lessons/delete_lesson.html', {'course': course, 'lesson': lesson})


# Thêm tài liệu vào bài học
@login_required
@teacher_required
def add_material(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.lesson = lesson
            material.save()
            return redirect(reverse('lesson_detail', args=[course.id, lesson.id]))
    else:
        form = LessonResourceForm()
    return render(request, 'lessons/add_material.html', {'form': form, 'course': course, 'lesson': lesson})

@login_required
@teacher_required
def delete_material(request, course_id, lesson_id, resource_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    material = get_object_or_404(LessonResource, id=resource_id, lesson=lesson)
    
    if request.method == 'POST':
        material.delete()
        return redirect('lesson_detail', course_id=course.id, lesson_id=lesson.id)
    
    return render(request, 'lessons/delete_material.html', {'course': course, 'lesson': lesson, 'material': material})