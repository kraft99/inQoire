from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.utils.http import is_safe_url
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse

from inqoire.account import is_post,post_data
from inqoire.users.models import User as inQoireUser,Activation
from inqoire.utils.decorators import unauthenticated
# from .auth import auth_credentials
from .forms import LoginForm,RegisterForm

User = get_user_model()




# logout view
@login_required
def logout(request):
	auth.logout(request)
	return redirect('/')


# Helper

# def is_post(request):
# 	# checks POST request
# 	return request.method == 'POST'


# def post_data(request):
# 	# form(request.POST)
# 	if is_post(request):
# 		return request.POST
# 	return None


# register view
@unauthenticated
def register(request,template='account/register.html',**kwargs):
	# TODO : Google Recapture.
	form = RegisterForm()
	if is_post(request):
		form = RegisterForm(data=post_data(request))
		if form.is_valid():
			email = form.cleaned_data.get('email')
			form.save(request=request)
			# session message 
			request.session['message'] = True

			ALLOW_CONFIRMATION = getattr(settings,'ALLOW_CONFIRMATION',False)
			if ALLOW_CONFIRMATION:
				# for production settings.
				return redirect(reverse('account:confirmation-reminder',kwargs={'email':email}))
			return redirect('account:login')
			# allow users to login.
		else:
			pass
	return TemplateResponse(request,template,{'form':form})



# login view
@sensitive_post_parameters()
@never_cache
@csrf_protect
@unauthenticated
def login(request):
	print(request.session.get('message',False))
	# session.
	if is_post(request):
		next = request.GET.get('next')
		form = LoginForm(data = post_data(request))
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = None
			try:
				user = auth.authenticate(username=username,password=password)
				# user = auth_credentials(username,password)
			except:
				pass
			if not user is None and user.is_active:
				if user.free_subscription_ended:
					mssg  = 'Sorry Your Free Subscription has ended. \
								 Subscribe with Credit Card 🙂'
					# messages.add_message(request,messages.INFO,mssg)
					# return redirect('account:login')
					return HttpResponse(mssg)
				if user.free_subscription_ended:
					user.is_active = False
					user.save()
					auth.logout(request)
					return redirect('/')
				auth.login(request,user)
				request.session['username'] = user.username

				if next:
					redirect_path = next
					is_a_safe_url = is_safe_url(url=redirect_path,
						allowed_hosts=request.get_host(),
						require_https=request.is_secure(),)
					if is_a_safe_url and redirect_path:
						return redirect(redirect_path)
					return redirect('/')
				return redirect('/')
			else:
				mssg = 'Invalid user credentials,\
					please check your username or password.'
				messages.add_message(request,messages.ERROR,mssg)
				return redirect('account:login')
		else:
			mssg = 'Invalid user credentials,\
					please check your username or password.'
			messages.add_message(request,messages.ERROR,mssg)
			return redirect('account:login')
	form = LoginForm()
	return TemplateResponse(request,'account/login.html',{'form':form})




def validate_confirmation_token(request,**kwargs):
	# NOTE : views must be slim :)
	# Refactor and move some codes out.
	if kwargs['token']:
		activation = get_object_or_404(Activation,token__iexact=kwargs.get('token'))
		if activation.is_expired():
			return HttpResponse('Activation code has expired.')
		from django.utils import timezone
		from dateutil.relativedelta import relativedelta
		user = activation.user
		user.is_active = True
		now = timezone.now()
		free_subsciption_expires = now + relativedelta(months = 1)
		user.activated_on = now
		user.free_subscription_ends_on = free_subsciption_expires
		user.save()
		activation.delete() #delete activation object.
		return redirect('account:login')

	return HttpResponse('login now,reditect to login page.')




def confirm_via_email(request,email):
	# TODO : Make it one time.with a hash url.
	email = get_object_or_404(inQoireUser,email__iexact=email).email
	return TemplateResponse(request,'mail/inform_registered_user.html',{'email':email})