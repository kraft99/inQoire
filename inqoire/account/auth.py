import re

from django.contrib import auth
from django.core.exceptions import ValidationError

from inqoire.users.models import User 



def auth_credentials(username,password):
	'''
	@purpose:
	This function accepts a two args.
	*username.
	This field can be either an actual username,email or a phone number.
	*password.
	@return
	user object 
	
	Regex. validate - username and email and phone number.
	if username matches that of a username_regex then its a username input
	if email matches that of an email regex then its an email input
	if phone number matches that of a phone number regex then its a phone number

	NOTE:
	with this Trick i can authenticate with any field.
	'''
	if is_valid_email(username):
		# Its an email.
		user = User.objects.filter(email__iexact=username).first()
		auth_user = auth.authenticate(username=user.username,password=password)

	elif is_valid_phone_number(username):
		# Its a phone number.
		user = User.objects.filter(phone_number__iexact=username).first()
		auth_user = auth.authenticate(username=user.username,password=password)

	elif is_valid_username(username):
		# email
		user = User.objects.filter(username__iexact=username).first()
		auth_user = auth.authenticate(username=user.username,password=password)

	return auth_user



def is_valid_email(value):
	from django.core.validators import validate_email
	try:
		validate_email(value)
	except ValidationError:
		return False
	return True


def is_valid_username(value):
	if re.match(r'^[\w.-]+$',value):
		return True
	return False

	
def is_valid_phone_number(value):
	# TODO:
	# use phone number regex 🙂.
	# no internet to search for regex.
	if value.startswith('0'):
		return True
	return False

