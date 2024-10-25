from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Trang chủ
    path('about/', views.about, name='about'),  # Trang Giới thiệu
    path('contact/', views.contact, name='contact'),  # Trang Liên hệ
    path('404/', views.error_404, name='404'),  # Trang 404
    path('403/', views.error_403, name='403'),  # Trang 403
]
