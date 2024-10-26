# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from lms_project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('assignments/', include('assignments.urls')),
    path('', include('home.urls')), 
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static (settings.STATIC_URL, document_root = settings.STATIC_ROOT )
