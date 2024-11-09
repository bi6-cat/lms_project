
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
    path('show_all_assignment/<int:lesson_id>/', views.show_all_assignment, name='show_all_assignment'),

    # Cập nhật Assignment
    path('update/<int:pk>/', views.UpdateAssignmentView.as_view(), name='update_assignment'),

    # Tạo tài nguyên cho Assignment
    path('create_resource/<int:assignment>/', views.CreateAssignmentResourceView.as_view(), name='create_resource'),

    # Hiển thị lỗi
    path('show_error/', views.show_error, name='show_error'),

    # Thêm điểm cho Assignment
    path('add-mark/<int:pk>/', views.AddMarkView.as_view(), name='add_mark'),

    # Kiểm tra trạng thái nộp bài cho Assignment
    path('<int:id_assignment>/submission-status/', views.assignment_submission_status, name='assignment_submission_status'),

    # Xoá Assignment
    path('delete/<int:pk>/', views.DeleteAssignmentView.as_view(), name='delete_assignment'),
]
