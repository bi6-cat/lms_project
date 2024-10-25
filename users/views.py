# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm,  UserUpdateForm
from django.contrib.auth.forms import PasswordChangeForm

# Đăng ký người dùng
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đăng ký thành công!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# Đăng nhập người dùng
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Tên đăng nhập hoặc mật khẩu không chính xác.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

# Đăng xuất người dùng
def logout_view(request):
    logout(request)
    return redirect('login')


# Hiển thị và cập nhật thông tin cá nhân
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thông tin cá nhân thành công!')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

# Quản lý người dùng (chỉ dành cho giáo viên hoặc người có quyền)
@login_required
def user_management(request):
    if request.user.role != 'teacher':
        messages.error(request, 'Bạn không có quyền truy cập.')
        return redirect('profile')
    users = User.objects.all()
    return render(request, 'users/user_management.html', {'users': users})


# Hàm xử lý đổi mật khẩu
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Để giữ cho người dùng đăng nhập
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})