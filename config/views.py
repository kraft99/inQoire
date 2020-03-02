from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required

from inqoire.users.models import User as inQoireUser
from inqoire.question.models import Question
from inqoire.answer.models import Answer
from inqoire.contribute.models import Contribution
from inqoire.vote.forms import VoteForm
from inqoire.answer.forms import AnswerAddForm



def welcome_to_inqoire(request,**kwargs):
	
	# Manager for Question.objects.all()
	# all() - displays questions with answers .
	question_qs = Question.objects.all()
	# print(question_qs.first())

	
	# response = redirect('index')
	# print(response) 
	# access_token = 'test_access_token'
	# response.set_cookie('access_token',access_token,max_age=1000, httponly=True)

	# if request.session.get('username',None):
	# 	print(request.session['username'])



	# print(hasattr(request,'user'))
	# print(request.user)


	# session_key = 'seesion test'
	# if not request.session.get(session_key,False):
	# 	print('am called only ones')
	# 	request.session[session_key] = True
	
	ctx = dict()

	if request.session.get('message',False):
		ctx['message'] = request.session.get('message',False)
		# use a modal dialog to show message ` Welcome to inQoire`
		# message should be displayed only one's for every new user account.
		print('welcome message')


	# Forms.
	
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
    
