from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,HttpResponseForbidden
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
import json

from inqoire.utils.decorators import ajax_required
from inqoire.answer.models import Answer
from .models import Comment



@ajax_required
@login_required
@require_http_methods(["POST"])
def comment_post(request):
	user = request.user
	answer_id = request.POST.get('answer_id');
	answer = get_object_or_404(Answer,id__iexact=answer_id)
	comment_text = request.POST.get('comment_text') 
	comment_obj,_ = Comment.objects.get_or_create(user=user,
												answer=answer,
												content=comment_text)
	count = answer.answer_comments_count
	return JsonResponse({'comment_count':count})



def json_error_message(mssg):
	return HttpResponse(json.dump(dict(success=False,mssg=mssg)))