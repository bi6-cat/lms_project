
from django.urls import path
from assignments import views

from django.urls import path
from . import views

urlpatterns = [
    # Tạo Assignment cho Lesson
    path('add/<int:lesson_id>/', views.AssignmentCreateView.as_view(), name='create_assignment'),
    
    # Nộp Assignment
    path('submit/', views.SubmitAssignmentWiew.as_view(), name='submit_assignment'),
    path('submit/<int:assignment_id>/', views.SubmitAssignmentWiew.as_view(), name='submit_assignment'),

    # Hiển thị tất cả các Assignment
    path('', views.show_assignment, name='show_assignment'),

    # Hiển thị tất cả Assignment cho một Lesson

    # Cập nhật Assignment

    # Tạo tài nguyên cho Assignment

    # Hiển thị lỗi
    path('show_error/', views.show_error, name='show_error'),

    # Thêm điểm cho Assignment
    path('add-mark/<int:pk>/', views.GradeAssignmentView.as_view(), name='add_mark'),

    # Kiểm tra trạng thái nộp bài cho Assignment
    path('<int:id_assignment>/submission-status/', views.assignment_submission_status, name='assignment_submission_status'),
    path('add/<int:lesson_id>/', views.AssignmentCreateView.as_view(), name='create_assignment'),
    path('update/<int:pk>/', views.AssignmentUpdateView.as_view(), name='update_assignment'),
    # Xoá Assignment
    path('delete/<int:pk>/', views.DeleteAssignmentView.as_view(), name='delete_assignment'),
]
