
from django.urls import path
from assignments import views

urlpatterns = [
    # path('add/', views.create_assignment, name='create_assignment'),   
    path('add/<int:lession_id>/', views.AssignmentCreateView.as_view(), name='create_assignment'),
    path('submit/', views.SubmitAssignmentWiew.as_view(), name='submit_assignment'),
    path('', views.show_assignment, name='show_assignment'),
    path('submit/<int:assignment_id>/', views.SubmitAssignmentWiew.as_view(), name='submit_assignment'),
    
]