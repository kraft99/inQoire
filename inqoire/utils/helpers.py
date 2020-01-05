import os

from PIL import Image
from django.conf import settings
from django.utils.text import Truncator
from django.core.exceptions import ValidationError



# TODO : DRY

def file_upload_loc(instance,file_obj):
	file_ext = file_obj.split('.')[-1].lower()
	_file = 'question-by-{0}.{1}'.format(instance.asked_by.username,file_ext)
	return os.path.join('file',_file)



def file_answer_loc(instance,file_obj):
	file_ext = file_obj.split('.')[-1].lower()
	_file = 'answer-by-{0}.{1}'.format(instance.answer_by.username,file_ext)
	return os.path.join('file',_file)



def dp_upload_loc(instance,file_obj):
	file_ext = file_obj.split('.')[-1].lower()
	_file = '{0}-dp.{1}'.format(instance.owner.username,file_ext)
	return os.path.join('file/dps/',_file)