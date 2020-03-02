from django.db import transaction
from django import forms

from .models import Question
from .const import ASK_BY_PRIVACY
from ..utils import validate_uploaded_file

class QuestionForm(forms.ModelForm):
	text 	   = forms.CharField(widget=forms.Textarea,max_length=150,label='')
	file 	   = forms.FileField(label='',required=False,validators=[validate_uploaded_file])
	link 	   = forms.URLField(label='',max_length=350,required=False)
	asked_by_privacy = forms.ChoiceField(choices=ASK_BY_PRIVACY,label='')
	
	class Meta:
		model  = Question
		fields = ('text','link','file','asked_by_privacy',)


	def __init__(self,*args,**kwargs):
		super(QuestionForm,self).__init__(*args,**kwargs)
		self.fields['text'].widget.attrs.update({'placeholder':'You\'ve got a Question ?'})
		self.fields['text'].widget.attrs.update({'rows':'5','cols':'20'})
		self.fields['link'].widget.attrs.update({'placeholder':'(optional) Link to a precise source of question.'})