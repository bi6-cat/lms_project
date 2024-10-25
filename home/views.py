from django.shortcuts import render

def home(request):
    return render(request, 'home/index.html')  # Trang chủ

def about(request):
    return render(request, 'home/about.html')  # Trang Giới thiệu

def contact(request):
    return render(request, 'home/contact.html')  # Trang Liên hệ

def error_404(request):
    return render(request, '404.html')  # Trang Liên hệ

def error_403(request):
    return render(request, '403.html')  # Trang Liên hệ


