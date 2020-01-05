from inqoire.utils.slug_generator import unique_slug_generator
from inqoire.utils.functions import question_summary

from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

from .models import Question


@receiver(pre_save,sender=Question)
def pre_save_post_receiver(sender,instance,*args,**kwargs):

	if not instance.slug:
		instance.summary = question_summary(instance.text)
		instance.slug = unique_slug_generator(instance)