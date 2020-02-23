from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django import forms

# test celery task
from inqoire.task.test import test_count

from inqoire.utils.ip import visitor_ip_address
from inqoire.users.models import User,Activation



class LoginForm(forms.Form):
	username     	= forms.CharField(label="username",required=True,widget=forms.TextInput())
	password 	    = forms.CharField(label="password",widget=forms.PasswordInput())
	

	def __init__(self,*args,**kwargs):
		super(LoginForm,self).__init__(*args,**kwargs)
		self.fields['username'].widget.attrs.update({'placeholder':'Your email or username or phone number'})
		self.fields['password'].widget.attrs.update({'placeholder':'Your password'})



class RegisterForm(UserCreationForm):
	email 	   	 = forms.EmailField(label='Email',required=True,widget=forms.EmailInput())
	phone_number = forms.CharField(label="Phone Number",required=True,widget=forms.TextInput())
	username     	= forms.CharField(label="username",required=True,widget=forms.TextInput())


	def __init__(self,*args,**kwargs):
		super(RegisterForm,self).__init__(*args,**kwargs)
		self.fields['email'].widget.attrs.update({'placeholder':'Your Email'})
		self.fields['phone_number'].widget.attrs.update({'placeholder':'Your Phone Number'})
		self.fields['username'].widget.attrs.update({'placeholder':'Your Username'})
		self.fields['password1'].widget.attrs.update({'placeholder':'Password'})
		self.fields['password2'].widget.attrs.update({'placeholder':'Confirm Password'})


	class Meta:
		model  = User
		fields = ('phone_number','email','username',)


	def clean_username(self):
		# TODO : Ban usernames
		username = self.cleaned_data.get('username').lower()
		qry = User.objects.filter(username__iexact=username)
		if qry.exists():
			# print('username exists')
			raise forms.ValidationError('user with username already exists.')
		return username



	def clean_email(self):
		email = self.cleaned_data.get('email',None)
		try:
			user_with_email = User.objects.get(email__iexact=email.lower())
		except User.DoesNotExist:
			return email
		# print('email exists')
		raise forms.ValidationError('user with email already exists.')



	def clean_phone_number(self):
		phone_number = self.cleaned_data.get('phone_number')
		try:
			user_with_phn = User.objects.get(phone_number__iexact=phone_number)
		except User.DoesNotExist:
			return phone_number
		# print('phone number exists')
		raise forms.ValidationError('user with phone number already exists.')


	def clean_password(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password2 and password1:
			if not (password2 == password1):
				print('password dont match')
				raise forms.ValidationError('password\'s do not match.')
			return password2


	@transaction.atomic
	def save(self,request=None,force_insert=False, force_update=False, commit=True):
		'''
		create user instance and ;
		0. set ip (registered users - info about location,device,browser etc.)
		1.set user.is_active = False
		2.send mail

		NOTE: request object can now be accessed in the forms and also in the models.
		by override of either save() in the forms or models.
		Googling it,'it could not be done.' by Anon. :) but i did't any where.
		'''
		

		user = super().save(commit=False)
		from django.conf import settings
		ALLOW_CONFIRMATION = getattr(settings,'ALLOW_CONFIRMATION',False)
		if ALLOW_CONFIRMATION:
			user.is_active = False #deactivate user model
		if not request is None:
			user.joined_from_ip = visitor_ip_address(request)
		if commit:
			user.save()
			# test_count(10)
			# test_count.delay(10)
			# create activation code and send it.
			if ALLOW_CONFIRMATION:
				Activation.create_activation_token(user).send(request=request)
		return user