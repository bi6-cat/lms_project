
from django.urls import path
from exams import views
from exams.views import AddExamView, EditExamView, DeleteExamView, EditExamKeyView, DeleteExamKeyView, SubmitAnswerView, cham_tat_ca, get_key, show_exam


urlpatterns = [
    path('<int:exam_id>/detail/', views.exam_detail, name='exam_detail'),
    path('add/<int:course_id>/', AddExamView.as_view(), name='add_exam'),
    path('edit/<int:pk>/', EditExamView.as_view(), name='edit_exam'),
    path('delete/<int:pk>/', DeleteExamView.as_view(), name='delete_exam'),
    path('exam/<int:exam_id>/edit_key/<int:pk>/', views.EditExamKeyView.as_view(), name='edit_key'),
    path('delete_key/<int:pk>/', DeleteExamKeyView.as_view(), name='delete_key'),
    path('get_key/<int:exam_id>/',get_key, name='get_key'),
    path('show_exam/<int:course_id>/', show_exam, name='show_exam'),
    path('submit_answer/<int:exam_id>/', SubmitAnswerView.as_view(), name='submit_answer'),
    path('grade_all/<int:exam_id>/', cham_tat_ca, name='grade_all'),
    path('delete_all_keys/<int:exam_id>/', views.delete_all_exam_keys, name='delete_all_exam_keys'),

]
