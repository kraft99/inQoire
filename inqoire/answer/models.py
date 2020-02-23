# @purpose - App handles inQoire Answers *
from django.contrib.humanize.templatetags.humanize import naturaltime
from inqoire.utils.helpers import file_answer_loc
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from django.db import models

from inqoire.question.models import Question



class Answer(models.Model):

	answer_by 		= models.ForeignKey(settings.AUTH_USER_MODEL,
										related_name='answers_by',
										on_delete=models.SET_NULL,
										blank=True,
										null=True)

	question 		= models.ForeignKey(to=Question,
										related_name='answers',
										on_delete=models.CASCADE)

	slug            = models.SlugField(max_length=150,unique=True,null=True,blank=True)

	text			= models.TextField(max_length=500)

	file 			= models.ImageField(upload_to=file_answer_loc,blank=True,null=True)

	upvotes 		= models.PositiveSmallIntegerField(default=0)
	downvotes 		= models.PositiveSmallIntegerField(default=0)
	views 			= models.PositiveSmallIntegerField(default=0,blank=True,null=True)
	answered_on 	= models.DateTimeField(blank=False,null=True)


	created 		= models.DateTimeField(auto_now_add=True)
	updated 		= models.DateTimeField(auto_now=True)



	class Meta:
		ordering 	 = (('upvotes'),)
		verbose_name = 'Answer'
		verbose_name_plural = 'Answers'


	def __str__(self):
		if self.answer_by is None:
			return "({0}) answered question '{1}' by ({2})".format('Anon',
										str(self.question.text[:55]),
										self.question.asked_by.username)
		return "({0}) answered question '{1}' by ({2})".format(self.answer_by.username,
										str(self.question.text[:55]),
										str(self.question.asked_by.username))


	def save(self,*args,**kwargs):
		from django.utils.text import slugify
		if not self.slug:
			if not self.answer_by is None:
				self.slug = slugify("%s-question-%s" % (self.text[:100],self.question.id), allow_unicode=True)
			#self.slug = slugify(f"anon-{self.text[:100]}",
			# 							to_lower=True,max_length=150)
		super(Answer,self).save(*args,**kwargs)


	def get_absolute_url(self):
		return reverse('answer:answer-view',args=[str(self.slug)])


	@property
	def url(self):
		return self.get_absolute_url()
	

	@property
	def pretty_date(self):
		if self.answered_on:
			return self.answered_on.strftime('%d %b')
		return


	def human_readable_timestamp(self):
		return humanize(self.created)

	timestamp = property(human_readable_timestamp)


	@property
	def file_url(self):
		if self.file:
			return self.file.url
		return


	@property
	def answer_comments_count(self):
		if self.comments:
			return self.comments.count()
		return
	
	
	


