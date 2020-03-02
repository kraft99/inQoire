# @purpose - App handles inQoire Questions *


import datetime
from django.utils import timezone

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.core.cache import cache # use and why ?
from django.conf import settings
from django.http import Http404
from django.urls import reverse
from django.db.models import Q,F
from django.db import models

from inqoire.utils.helpers import file_upload_loc
from . import const


# Querset class
class QuestionQuerySet(models.QuerySet):
    # Queryset - returns most voted on question answers.

    def all(self):
        # shows only questions with is answered mark True.
        return self.filter(is_answered=True)

    def most_voted_question_answers(self):
        pass

# Queryset Manager
class QuestionManager(models.Manager):

    def get_queryset(self):
        # Queryset - chaining purposes.
        return QuestionQuerySet(self.model,using=self._db)

    def all(self):
        return self.get_queryset().all()

    def most_voted_question_answers(self):
        return self.get_queryset().most_voted_question_answers()


class Question(models.Model):
    """
    @model - Question Model.

    @params;
    asked_by - User
    text     - Text
    summary  - Text
    slug     - Text
    file     - File 
    is_answered - Boolean
    asked_by_privacy - Interger

    
    @how
    - is_answered
    1. Questions with votes counts exceeding 4 will be marked as is_answered
    2. Ranking which answer gets showed will be based on a simple algorithm I have to implement.

    """
    asked_by                    = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                    related_name='questions',
                                    blank=False,
                                    null=False,
                                    on_delete=models.CASCADE)

    text                    	= models.TextField(max_length=400)
    summary 					= models.CharField(max_length=250,blank=True,null=True)
    link 						= models.URLField(max_length=300,blank=True,null=True) # optional - link gives context
    slug                        = models.SlugField(max_length=300,unique=True,null=True,blank=True,db_index=True)
    file                        = models.ImageField(upload_to=file_upload_loc,blank=True,null=True)
    is_answered                 = models.BooleanField(default=False) #most voted answer is accepted as answer

    asked_by_privacy 			= models.PositiveSmallIntegerField(choices=const.ASK_BY_PRIVACY,blank=False,null=True,default=const.PUBLIC)
    
    created                     = models.DateTimeField(auto_now_add=True)
    updated                     = models.DateTimeField(auto_now=True)

    objects                     = QuestionManager()


    class Meta:
    	ordering 				= ('-created',)
    	verbose_name			= 'Question'
    	verbose_name_plural     = 'Questions'


    def __str__(self):
    	return '{0} posted a question "{1}" '.format(self.asked_by.username,self.text[:25])


    def save(self,*args,**kwargs):
        super(Question,self).save(*args,**kwargs)


    def get_absolute_url(self):
        return reverse('question:question_detail',args=[str(self.slug)])

    qst_detail_url = property(get_absolute_url)
    

    @property
    def most_upvote_answer(self):
        """
        - if a quuestion has anwers filter, the anwers with upvotes greater than N.
        """
        VALUE = 4
        if self.answers:
            # give as the first answer to this questions.
            # probably thats the mos voted and right one.
            return self.answers.filter(upvotes__gte=VALUE).first()
        return None


    @property
    def file_url(self):
        if self.file:
            return self.file.url
        return



    def human_readable_timestamp(self):
        # better human readable timestamp eg. 2 min ago ..
        return humanize(self.created)
    timestamp = property(human_readable_timestamp)


    @property
    def answers_count(self):
        # a count of total answers given for question.
        return self.answers.count()
    
    