
from django.urls import path
from exams.views import AddExamView, EditExamView, DeleteExamView, AddExamKeyView, EditExamKeyView, DeleteExamKeyView, transform_answer, show_exam


urlpatterns = [
    path('add/<int:course_id>/', AddExamView.as_view(), name='add_exam'),
    path('edit/<int:course_id>/', EditExamView.as_view(), name='edit_exam'),
    path('delete/<int:pk>/', DeleteExamView.as_view(), name='delete_exam'),
    path('add_key/<int:exam_id>/', AddExamKeyView.as_view(), name='add_key'),
    path('edit_key/<int:pk>/', EditExamKeyView.as_view(), name='edit_key'),
    path('delete_key/<int:pk>/', DeleteExamKeyView.as_view(), name='delete_key'),
    path('get_key/<int:exam_id>/',transform_answer , name='get_key'),
    path('show_exam/<int:course_id>/', show_exam, name='show_exam'),

]
