# @purpose - App handles inQoire Questions *

from django.conf import settings
from django.db import models

from inqoire.question.models import Question


class Contribution(models.Model):

	by 	= models.ForeignKey(to=settings.AUTH_USER_MODEL,
							related_name='contribs',
							on_delete=models.CASCADE,
							blank=True,
							null=True)

	question = models.ForeignKey(to=Question,
								related_name='+',
								on_delete=models.CASCADE,
								blank=True,
								null=True)

	users	= models.ManyToManyField(to=settings.AUTH_USER_MODEL,
									related_name='contributors',
									blank=True)

	contrib_on = models.DateTimeField(blank=True,null=True)

	created = models.DateTimeField(auto_now_add=True)


	class Meta:
		ordering = ('-created',)
		verbose_name = 'Contribution'
		verbose_name_plural = 'Contributions'

	def __str__(self):
		if self.by:
			return '{0} contributed to {1}'.format(self.by.username,self.question.text[:100])
		return




'''
This is not the best way to handle users contribution.
For the sake of an exercise and time,let keep it this way.
Our secret 🙂.

How i intend using it.
# For any answer a user provides a contribution object is created\
for that question and user.
'''
def create_contribution(question,user,datetime_obj=None):
	from django.utils import timezone
	if datetime_obj is None:
		datetime_obj = timezone.now()
	qry = Contribution.objects.filter(by=user,question=question)
	if qry.exists():
		# CASES : user might want to add more than one answer.
		# create but dont duplicate users (might raise error.)
		Contribution.objects.create(by=user,question=question)
	else:
		# craete and add user to users
		contrib,_ = Contribution.objects.get_or_create(by=user,question=question)
		contrib.users.add(user)






