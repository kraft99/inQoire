from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse,Http404
from django.utils.http import is_safe_url
from django.contrib import auth
from django.urls import reverse
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import render,redirect

from inqoire.users.models import User as inQoireUser,Activation
from .auth import auth_credentials
from .forms import LoginForm,RegisterForm

User = get_user_model()



# logout view
@login_required
def logout(request):
	auth.logout(request)
	return redirect('/')


# register view
def register(request):
	# TODO : Google Recapture.
	current_user = request.user
	if current_user.is_authenticated and current_user.is_active:
		return redirect('/')
	if request.method == 'POST':
		form = RegisterForm(data=request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			form.save(request=request)
			ALLOW_CONFIRMATION = getattr(settings,'ALLOW_CONFIRMATION',False)
			if ALLOW_CONFIRMATION:
				# for production settings.
				return redirect(reverse('account:confirmation-reminder',kwargs={'email':email}))
			return redirect('account:login')
			# allow users to login.
		else:
			print('invalid form')
	form = RegisterForm()
	return TemplateResponse(request,'account/register.html',{'form':form})



# login view
def login(request):
	# request.session['u'] = 'red'
	current_user = request.user
	if current_user.is_authenticated and current_user.is_active:
		return redirect('/')
	# session.
	if request.method == 'POST':
		next = request.GET.get('next')
		form = LoginForm(data = request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			# user = auth.authenticate(username=username,password=password)
			user = None
			try:
				user = auth_credentials(username,password)
			except:
				pass
			if not user is None and user.is_active:
				# check for free subscription expiration.
				if user.free_subscription_ended:
					return HttpResponse('Sorry Your Free Subscription has ended. Subscribe with Credit Card 🙂')
				# assume user is logged-in already but subscription has ended.Logout that user :)
				if user.free_subscription_ended:
					user.is_active = False
					user.save()
					auth.logout(request)
					return redirect('/')
				# print(user.free_subscription_ended)
				auth.login(request,user)
				if next:
					# print(next)
					redirect_path = next
					is_a_safe_url = is_safe_url(url=redirect_path,
						allowed_hosts=request.get_host(),
						require_https=request.is_secure(),)
					# print(request.is_secure()) # why not a secured request ? Google it !
					if is_a_safe_url and redirect_path:
						return redirect(redirect_path)
					return redirect('/') #if not safe path
				return redirect('/')
			else:
				print('failed to login user')
				return redirect('account:login')
		else:
			print('invalid data')
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