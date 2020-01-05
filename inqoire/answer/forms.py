from django.db import transaction
from django import forms

from .models import Answer


class AnswerAddForm(forms.ModelForm):
	answer_by  = forms.CharField(widget=forms.HiddenInput)
	question   = forms.CharField(widget=forms.HiddenInput)
	# text 	   = forms.CharField(max_length=250,label='')
	text 	   = forms.CharField(widget=forms.Textarea,max_length=150,label='')

	class Meta:
		model  = Answer
		fields = ('answer_by','question','text',)


	def __init__(self,*args,**kwargs):
		super(AnswerAddForm,self).__init__(*args,**kwargs)
		self.fields['text'].widget.attrs.update({'placeholder':'You\'ve a better answer for this Question ?'})
		self.fields['text'].widget.attrs.update({'rows':'3','cols':'14'})