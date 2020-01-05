from django.utils import timezone

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from inqoire.utils.decorators import ajax_required

from inqoire.answer.models import Answer
from inqoire.question.models import Question
from inqoire.contribute.models import create_contribution
from inqoire.users.models import User as inQoireUser
# Create your views here.


@login_required
@ajax_required
@require_http_methods(["POST"])
def answer_add(request):
	username = request.POST.get('username')
	question_id = request.POST.get('question_id')

	ask_by = get_object_or_404(inQoireUser,username__iexact=username)
	question_obj = get_object_or_404(Question,id = question_id)
	text = request.POST.get('text')
	Answer(answer_by=ask_by,question=question_obj,
						text=text,answered_on=timezone.now()).save()
	#contribution created.
	create_contribution(question_obj,ask_by)
	data = {'successful':True}
	return JsonResponse(data)



def answer_view(request,slug):
	from inqoire.utils.functions import viewed_by_session
	answer_obj = get_object_or_404(Answer,slug__iexact=slug)
	viewed_by_session(request,answer_obj)
	return redirect('/')