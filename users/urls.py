# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('user-management/', views.user_management, name='user_management'), # quản lý học sinh cho giáo viên
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
