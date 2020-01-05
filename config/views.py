from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required

from inqoire.users.models import User as inQoireUser
from inqoire.question.models import Question
from inqoire.answer.models import Answer
from inqoire.contribute.models import Contribution
from inqoire.vote.forms import VoteForm
from inqoire.answer.forms import AnswerAddForm



def welcome_to_inqoire(request,**kwargs):
	
	question_qs = Question.objects.all()[:4]#TODO Filter by Most Answered
	# Forms.
	ctx = dict()
	ctx['vote_form'] = VoteForm()
	ctx['answer_form'] = AnswerAddForm(initial={'answer_by':request.user})

	ctx['questions'] = question_qs
	questions_count = Question.objects.count()
	answer_count	= Answer.objects.count()
	ctx['q_count'] = questions_count
	ctx['a_count'] = answer_count
	ctx['contribution_count'] = Contribution.objects.count()
	ctx['users_count'] = inQoireUser.objects.count()
	ctx['superuser'] = inQoireUser.objects.first()
	return TemplateResponse(request,'index.html',ctx)
    
