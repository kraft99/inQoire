import os
import uuid

import datetime
from dateutil.relativedelta import relativedelta

from django.utils.text import Truncator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text



def question_summary(text):
	if text:
		return Truncator(text).chars(130)
	return


EXPIRE_ACTIVATION_WEEKS = 1

def date_expired(now = datetime.datetime.now()):
	return now + relativedelta(weeks = EXPIRE_ACTIVATION_WEEKS)


def activation_token():
	token_ = str(uuid.uuid4()).replace('-','')
	return urlsafe_base64_encode(force_bytes(token_))




def viewed_by_session(request,answer_obj):
	# handles post viewers counter -> use REDIS
	session_key = 'viewed_topic_{}'.format(answer_obj.id)
	if not request.session.get(session_key,False):
		answer_obj.views += 1
		answer_obj.save()
		request.session[session_key] = True
