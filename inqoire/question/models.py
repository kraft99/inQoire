# @purpose - App handles inQoire Questions *


import datetime
from django.utils import timezone


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




class Question(models.Model):

    asked_by                    = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                    related_name='questions',
                                    blank=False,
                                    null=False,
                                    on_delete=models.CASCADE)

    text                    	= models.TextField(max_length=400)
    summary 					= models.CharField(max_length=250,blank=True,null=True)
    link 						= models.URLField(max_length=300,blank=True,null=True) # optional - link gives context
    slug                        = models.SlugField(max_length=300,unique=True,null=True,blank=True)
    file                        = models.ImageField(upload_to=file_upload_loc,blank=True,null=True)
    is_answered                 = models.BooleanField(default=False) #most voted answer is accepted as answer

    asked_by_privacy 			= models.PositiveSmallIntegerField(choices=const.ASK_BY_PRIVACY,blank=False,null=True,default=const.PUBLIC)
    
    created                     = models.DateTimeField(auto_now_add=True)
    updated                     = models.DateTimeField(auto_now=True)



    class Meta:
    	ordering 				= ('-created',)
    	verbose_name			= 'Question'
    	verbose_name_plural     = 'Questions'


    def __str__(self):
    	return '{0} posted a question "{1}" '.format(self.asked_by.username,self.text[:25])

    # def save(self,*args,**kwargs):
    #     super(Question,self).save(*args,**kwargs)
    

    @property
    def most_upvote_answer(self):
        # TODO - algorithm to rank most accepted answers by votes count and views and comment (+ive sentiment)
        # Show only the mosted accpted `one` as first answer,other related answers can be found on click to view other soln.
        if self.answers:
            return self.answers.filter(upvotes__gte=3).first()
        return None


    @property
    def answers_count(self):
        return self.answers.count()
    
    