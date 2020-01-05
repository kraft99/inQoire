#@purpose - App handles inQoire user connections.

from django.db import models
from inqoire.users.models import User


class Connection(models.Model):

	to_user 	= models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='from_user')
	from_user 	= models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='to_user')

	created     = models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)


	class Meta:
		unique_together = (('to_user','from_user'),)


	def save(self,*args,**kwargs):
		is_self = self.to_user == self.from_user
		if is_self:
			raise ValueError('You can\'t connect to yourself 🙂')
		super(Connection,self).save(*args,**kwargs)


	def __str__(self):
		return '{0} has connected with {1}'.format(self.from_user.username,
														self.to_user.username)


	@classmethod
	def people_user_has_connected_to(cls,user):
		''' Returns a QuerySet rep. users that the checked `user` has connected to. '''
		qry = cls.objects.filter(from_user=user).values_list('to_user',flat=True)
		return User.objects.filter(id__in=qry)



	@classmethod
	def people_connected_to_user(cls,user):
		''' Returns a QuerySet rep. users that the checked `user` has been connected with. '''
		qry = cls.objects.filter(to_user=user).values_list('from_user',flat=True)
		return User.objects.filter(id__in=qry)



	@classmethod
	def mutual_connections(cls,user):
		''' Returns a QuerySet rep. users that the checked `user` as a mutual connection with. '''
		pass



	@classmethod
	def create_connection(cls,from_user,to_user):
		''' Creates a connection b/n two users. '''
		pass


	@classmethod
	def user_connectors(cls,user):
		pass