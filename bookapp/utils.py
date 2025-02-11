from functools import wraps

from django.utils import timezone

from bookapp.responses import LibraryError


def method_required(allowed_methods):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method not in allowed_methods:
                return LibraryError.to_json_response(
                    LibraryError.INVALID_API,
                    f"This endpoint only allow method {', '.join(allowed_methods)}."
                )
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def get_current_datetime():
    now = timezone.now()
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_datetime
