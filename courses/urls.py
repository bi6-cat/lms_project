# courses/urls.py

from django.urls import path
from .views import *
from courses import views  # Import tất cả các view từ file views.py
# app_name = 'courses'  
urlpatterns = [
    path('', course_list, name='course_list'),  
    path('<int:course_id>/', course_detail, name='course_detail'),  
    path('add/', CourseCreateView.as_view(), name='add_course'),  
    path('<int:pk>/edit/', CourseUpdateView.as_view(), name='edit_course'),  
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='delete_course'),  
    path('<int:course_id>/enroll/', enroll_course, name='enroll_course'),
    path('<int:course_id>/unenroll/', unenroll_course, name='unenroll_course'),
    path('search/', search_courses, name='search_courses'),
    path('course/<int:course_id>/students/', views.enrolled_students_list, name='enrolled_students_list'),
]