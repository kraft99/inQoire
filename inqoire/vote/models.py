# @purpose - App handles inQoire Answers Votes *
import uuid
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.db import models


UP = +1
DOWN = -1

# mark safe(<tag></tag>) - render tags as normal HTML not as strings.
vote_choices = (
    (UP, mark_safe('<i class="la la-thumbs-up thumbs"></i>')),
    (DOWN,mark_safe('<i class="la la-thumbs-down thumbs"></i>')),
)


class Vote(models.Model):
	
	uuid_id 		 = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	user 			 = models.ForeignKey(to=settings.AUTH_USER_MODEL,related_name='vote',on_delete=models.CASCADE)
	value 			 = models.PositiveSmallIntegerField(choices=vote_choices)
	content_type	 = models.ForeignKey(ContentType, on_delete=models.CASCADE,limit_choices_to=\
																				{'model__in':('answer',)}) #Model
	object_id 		 = models.PositiveIntegerField() # instance id
	content_object   = GenericForeignKey("content_type", "object_id")

	created 		 = models.DateTimeField(auto_now_add=True)


	class Meta:
		verbose_name = 'Vote'
		verbose_name_plural = 'Votes'
		index_together = ("content_type", "object_id")
		unique_together = ("user", "content_type", "object_id")
  