from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *arg, **kwarg):
        if request.user.is_authenticated:
            return redirect ('/')
        else:
            return view_func(request, *arg,**kwarg)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *arg,**kwarg):
            group= None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func (request, *arg,**kwarg)
            else:
                return redirect('contact')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func (request, *arg,**kwarg):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'guest':
            return HttpResponse('acceso no autoriazado')
        if group == 'admin':
            return view_func (request, *arg,**kwarg)
 

    return wrapper_func

