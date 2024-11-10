# lessons/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('courses/<int:course_id>/lessons/', views.lesson_list, name='lesson_list'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('courses/<int:course_id>/lessons/add/', views.add_lesson, name='add_lesson'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/materials/add/', views.add_material, name='add_material'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/materials/<int:resource_id>/delete/', views.delete_material, name='delete_material'),
]
