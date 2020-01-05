from django.contrib.auth.models import User
from django.conf import settings
from django.http import Http404

from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save

from inqoire.answer.models import Answer
from django.db import models


class Comment(models.Model):

	user 			= models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comment_by')
	answer 			= models.ForeignKey(to=Answer,on_delete=models.CASCADE,related_name='comments')
	content 		= models.CharField(max_length=255)
	created 		= models.DateTimeField(auto_now_add=True)
	update			= models.DateTimeField(auto_now=True)



	class Meta:
		ordering 			= ('-created',)
		verbose_name		= 'Comment'
		verbose_name_plural = 'Comments'


	def __str__(self):
		return "{0} made a comment.".format(self.user.username)

	

    



