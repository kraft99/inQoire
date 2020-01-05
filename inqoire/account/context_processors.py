


def is_auth(request):
	flag = False
	if request.user.is_authenticated:
		flag = True
	return {'is_auth':flag}


