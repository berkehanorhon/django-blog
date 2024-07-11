from functools import wraps

from django.shortcuts import redirect


def LOGOUT_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return function(request, *args, **kwargs)

    return wrap


def author_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user, 'is_author', False):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')

    return _wrapped_view
