from django.http import HttpResponseBadRequest
from django.contrib.auth import REDIRECT_FIELD_NAME
from inqoire.utils.exceptions import PermissionDeniedError
from django.contrib.auth.decorators import user_passes_test
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
	@ decorator - redirects authenticated users to index route on page load 
	or login rout for un-auth users
	'''
	def wrap(request,*args,**kwargs):
		if request.user.is_authenticated and request.user.is_active:
			return redirect(reverse('index'))
		else:
			return f(request,*args,**kwargs)

	wrap.__doc__ = f.__doc__
	wrap.__name__ = f.__name__
	return wrap

