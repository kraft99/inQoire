
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.contrib.auth import REDIRECT_FIELD_NAME
from inqoire.utils.exceptions import PermissionDeniedError
from django.contrib.auth.decorators import user_passes_test

# try this imports
from django.contrib.auth.views import redirect_to_login
from functools import wraps

from inqoire.users.models import User as inQoireUser
from django.shortcuts import redirect
from django.urls import reverse


def ajax_required(f):
    """A nice decorator to validate that a browser request is AJAX"""
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def is_authenticated_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect_to_login(next=request.get_full_path(),
                                     login_url=settings.LOGIN_URL)
        return view_func(request, *args, **kwargs)

    return wrapper




def staff_required(function=None,redirect_field_name=REDIRECT_FIELD_NAME,login_url='account:login'):
	""" Decorator for views that checks that logged in user is a staff/admin.
	Redirects to login pag if neccessary.
	
	@staff_required
	def view_func(request,***kwargs):
		pass

	"""
	actual_decorator = user_passes_test(
		lambda u: u.is_active and u.is_staff,
		login_url = login_url,
		redirect_field_name=redirect_field_name
		)
	if function:
		return actual_decorator(function)
	return actual_decorator



def superuser_required(function=None,redirect_field_name=REDIRECT_FIELD_NAME,login_url='account:login'):
	""" Decorator for views that checks that logged in user is a superuser/admin.
	Redirects to login pag if neccessary.
	
	@superuser_required
	def view_func(request,***kwargs):
		pass

	"""
	actual_decorator = user_passes_test(
		lambda u: u.is_active and u.is_superuser,
		login_url = login_url,
		redirect_field_name=redirect_field_name
		)
	if function:
		return actual_decorator(function)
	return actual_decorator




	""" This decorator for view checks that login user is owner of private page eg. edit or delete profile.
	@owner_required
	def view_func(request,***kwargs):
		pass

	"""
def owner_required(f):
    def wrap(request, *args, **kwargs):
        user_obj = inQoireUser.objects.get(username=kwargs['username'])
        if request.user == user_obj:
            return f(request, *args, **kwargs)
        else:
            raise PermissionDeniedError('You don\'t have permission to perform action.')

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap



def unauthenticated(f):
	'''
	This decorator minimises codes written in views to redirect authenticated user to home page

	BEFORE
	def view_fun(request):
		if request.user.is_authenticated:
			return redirect(reverse('index'))

	NOW

	@unauthenticated
	def view_fun(request):
		pass

	'''
	def wrap(request,*args,**kwargs):
		if request.user.is_authenticated and request.user.is_active:
			return redirect(reverse('index'))
		else:
			return f(request,*args,**kwargs)

	wrap.__doc__ = f.__doc__
	wrap.__name__ = f.__name__
	return wrap



def guest_only(view_func):
    # TODO: test!
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(request.GET.get('next', request.user.st.get_absolute_url()))

        return view_func(request, *args, **kwargs)

    return wrapper
