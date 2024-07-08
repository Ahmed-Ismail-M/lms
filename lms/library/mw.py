from django.http import HttpResponse


def auth_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            print(request.user)
            return HttpResponse("Not Authorized", status=401)
    return wrapper_func


def allowed_users(allowed_roles: list):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if request.user.groups.exists():
                if request.user.groups.all()[0].name in allowed_roles:
                    return view_func(request, *args, **kwargs)
            return HttpResponse("Not Authorized", status=401)

        return wrapper_func

    return decorator