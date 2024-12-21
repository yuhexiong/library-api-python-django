from functools import wraps
from http import HTTPStatus
from django.http import JsonResponse
from bookapp.errors import LibraryCode
from django.utils import timezone

def method_required(allowed_methods):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method not in allowed_methods:
                return JsonResponse(
                    {
                        'code': LibraryCode.INVALID_API.value, 
                        'message': f"This endpoint only allow method {', '.join(allowed_methods)}."
                    }, 
                    status=HTTPStatus.BAD_REQUEST
                )
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def get_current_datetime():
    now = timezone.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_datetime
