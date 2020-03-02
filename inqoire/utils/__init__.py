from django.core.exceptions import ValidationError




# Constant 
IMAGE_FILE_VALIDATION_EXTENSIONS = ['png','jpeg','jpg']
PDF_FILE_VALIDATION_EXTENSIONS = ['pdf']

def get_extension_type():
	return {
	'image':IMAGE_FILE_VALIDATION_EXTENSIONS,
	'pdf':PDF_FILE_VALIDATION_EXTENSIONS
	}


def validate_uploaded_file(uploaded):
	# validate both extension and file format at a time.
	try:
		validate_file_size(uploaded)
		validate_file_extension(uploaded)
	except ValidationError as e:
		return e
	return True

# validate uploaded file size
def validate_file_size(upload):
	limit = 1024 * 1024 * 1 # 1 MB
	if upload.size > limit:
		raise ValidationError('upload file size must not exceed 1 MB')
	return True # no error

# validate file extension
def validate_file_extension(upload):
	file_name = upload.name
	file_extension = file_name.lower().split('.')[-1]
	if file_extension not in get_extension_type()['image'] or \
	file_extension not in get_extension_type()['pdf']:
		message = '{0} extension not allowed'
		raise ValidationError(message.format(file_extension))
	return True


