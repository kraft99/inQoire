from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render,redirect
from django.urls import reverse

from inqoire.utils.decorators import ajax_required
from inqoire.answer.models import Answer



def vote(request):
	return HttpResponse('vote on most accepted answer.')