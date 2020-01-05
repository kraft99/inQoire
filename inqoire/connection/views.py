from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from inqoire.utils.decorators import ajax_required
from inqoire.users.models import User as inQoireUser

from .models import Connection


@ajax_required
@login_required
@require_http_methods(["POST"])
def switch_connection(request):
	from_user = request.POST.get('from_user')
	from_user = get_object_or_404(inQoireUser,username__iexact=from_user)
	to_user = request.POST.get('to_user')
	to_user = get_object_or_404(inQoireUser,username__iexact=to_user)
	connection_obj,flag = Connection.objects.get_or_create(to_user=to_user,from_user=from_user)
	is_connected = True
	if not flag:
		connection_obj.delete()
		is_connected = False
	data = {'is_connected':is_connected}
	return JsonResponse(data)