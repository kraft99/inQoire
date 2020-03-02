from django.utils import timezone

from django.http import HttpResponse,Http404,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from inqoire.utils.decorators import ajax_required

from inqoire.question.models import Question
from inqoire.users.models import User as inQoireUser
from inqoire.question.forms import QuestionForm
# from inqoire.utils.decorators import superuser_required

# Create your views here.


@login_required
# @superuser_required
def question_page(request,template='question/questions.html',**kwargs):
	qform = QuestionForm()
	if request.method == 'POST':
		qform = QuestionForm(data=request.POST,files=request.FILES)
		if qform.is_valid():
			instance = qform.save(commit=False)
			instance.asked_by = request.user
			instance.save()
			print('saved')
		else:
			print('invalid')
		return redirect('question:question-page')
	ctx = dict()
	ctx['qform'] = qform
	ctx['superuser'] = inQoireUser.objects.first()#test only
	return TemplateResponse(request,template,ctx)




def question_detail(request,template=None,**kwargs):
	if kwargs['slug']:
		slug = kwargs.pop('slug').strip()
		try:
			question = Question.objects.get(slug__iexact=slug)
		except Question.DoesNotExist:
			raise Http404()
		return HttpResponse(request.build_absolute_uri(question.qst_detail_url))
	else:
		raise Http404()


