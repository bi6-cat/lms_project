# courses/urls.py

from django.urls import path
from .views import *  # Import tất cả các view từ file views.py
# app_name = 'courses'  
urlpatterns = [
    path('', course_list, name='course_list'),  # Sử dụng class-based view
    path('<int:course_id>/', course_detail, name='course_detail'),  # Sử dụng class-based view
    path('add/', CourseCreateView.as_view(), name='add_course'),  # Sử dụng class-based view
    path('<int:pk>/edit/', CourseUpdateView.as_view(), name='edit_course'),  # Sử dụng class-based view
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='delete_course'),  # Sử dụng class-based view
    path('<int:course_id>/enroll/', enroll_course, name='enroll_course'),
    path('<int:course_id>/unenroll/', unenroll_course, name='unenroll_course'),
    path('search/', search_courses, name='search_courses'),
]