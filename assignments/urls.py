
from django.urls import path
from assignments import views

urlpatterns = [
    # path('add/', views.create_assignment, name='create_assignment'),   
    path('add/<int:lession_id>/', views.AssignmentCreateView.as_view(), name='create_assignment'),
    path('submit/', views.SubmitAssignmentWiew.as_view(), name='submit_assignment'),
    path('', views.show_assignment, name='show_assignment'),
    path('submit/<int:assignment_id>/', views.SubmitAssignmentWiew.as_view(), name='submit_assignment'),
    path('delete/<int:pk>/', views.DeleteAssignmentView.as_view(), name='delete_assignment'),
    path('show_all_assignment/<int:lession_id>/', views.show_all_assignment, name='show_all_assignment'),
    path('update/<int:pk>/', views.UpdateAssignmentView.as_view(), name='update_assignment'),
    path('create_resource/<int:assignment>/', views.CreateAssignmentResourceView.as_view(), name='create_resource'),
    path('show_error/', views.show_error, name='show_error'),
    path('add-mark/<int:pk>/', views.AddMarkView.as_view(), name='add_mark'),
    path('show-list-submit/<int:id_assignment>/', views.student_not_submit, name='show_list_submit'),
]