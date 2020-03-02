import os
import uuid

import datetime
from django.conf import settings
# from dateutil.relativedelta import relativedelta

from django.utils.text import Truncator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text



def question_summary(text):
	if text:
		return Truncator(text).chars(130)
	return


# def date_expired(now = datetime.datetime.now()):
# 	return now + relativedelta(weeks = EXPIRE_ACTIVATION_WEEKS)



def date_expired(now = datetime.datetime.now()):
	return now + datetime.timedelta(days=getattr(settings,'EXPIRE_ACTIVATION_DAYS',7))


def activation_token():
	token_ = str(uuid.uuid4()).replace('-','')
	return urlsafe_base64_encode(force_bytes(token_))




def viewed_by_session(request,answer_obj):
	# TODO : handles question-answer viewers counter -> use REDIS

	# sert session key in session
	session_key = 'viewed_{}'.format(answer_obj.id)
	# retrieve session key
	if not request.session.get(session_key,False):
		# session not found then
		# perform this action and set this session.
		# this is done only ones
		answer_obj.views += 1
		answer_obj.save()
		request.session[session_key] = True
