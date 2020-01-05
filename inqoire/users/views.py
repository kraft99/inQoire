from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.template.response import TemplateResponse

from inqoire.users.models import User as inQoireUser


# view for a inQoire user.
def view_by_user(request,**kwargs):
	user = get_object_or_404(inQoireUser,username__iexact=kwargs['username'].strip())
	return TemplateResponse(request,'user/profile.html',{'username':kwargs['username'],'user_obj':user})