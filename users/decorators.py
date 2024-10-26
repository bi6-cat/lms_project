from django.core.exceptions import PermissionDenied
from functools import wraps

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'teacher':
            raise PermissionDenied("Bạn không có quyền truy cập.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view