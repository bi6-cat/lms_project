# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.decorators import teacher_required
from .models import User, Student, Teacher
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm,  TeacherProfileForm, StudentProfileForm
from django.contrib.auth.forms import PasswordChangeForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            # Tạo Teacher hoặc Student dựa vào role
            if user.role == 'teacher':
                department = request.POST.get('department')
                Teacher.objects.create(user=user, department=department)
            elif user.role == 'student':
                school_name = request.POST.get('school_name')
                Student.objects.create(user=user, school_name=school_name)
            
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
                # Lấy tham số 'next' từ request.POST hoặc request.GET
                next_url = request.POST.get('next') or request.GET.get('next')
                # Chuyển hướng về 'next' nếu có, nếu không thì về trang mặc định 'home'
                return redirect(next_url or 'home')
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
    user = request.user

    if user.role == 'teacher':
        profile_form = TeacherProfileForm(instance=user.teacher)
    elif user.role == 'student':
        profile_form = StudentProfileForm(instance=user.student)
    else:
        profile_form = None  # Trường hợp không thuộc giáo viên hoặc học sinh

    user_form = UserProfileForm(instance=user)

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)

        if user.role == 'teacher':
            profile_form = TeacherProfileForm(request.POST, instance=user.teacher)
        elif user.role == 'student':
            profile_form = StudentProfileForm(request.POST, instance=user.student)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Điều hướng về trang hồ sơ sau khi lưu

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# Quản lý người dùng (chỉ dành cho giáo viên hoặc người có quyền)
@teacher_required
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

def reset_password(request):
    return render(request, 'users/reset_password.html')
