from django import forms
from .models import vote_choices as VOTE

class VoteForm(forms.Form):
	content_type 	= forms.CharField(widget=forms.HiddenInput)
	object_id 		= forms.CharField(widget=forms.HiddenInput)
	value 			= forms.ChoiceField(choices=VOTE,label="",required=False,widget=forms.RadioSelect())