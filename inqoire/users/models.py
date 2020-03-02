# @purpose - App handles inQoire User, Profile ... avatar,gravatar,dashboard

from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.db.models import F

from django.contrib.auth.models import AbstractUser
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError,send_mail
from django.db import models

from inqoire.utils.functions import activation_token,date_expired
# from inqoire.connection.models import Connection
from inqoire.account import build_absolute_uri
from inqoire.utils import helpers



class User(AbstractUser):
    ''' User Model.
    if actived_on is not None.
    Then based on when its acitvate ,set expire date to use site. 

    '''
    score   		            = models.PositiveSmallIntegerField(default=0,blank=True,null=True)
    phone_number                = models.CharField(max_length=16,blank=False,null=True,unique=True)
    joined_from_ip              = models.GenericIPAddressField(blank=True,null=True)
    last_seen_ip                = models.GenericIPAddressField(blank=True,null=True)
    activated_on                = models.DateTimeField(blank=True,null=True) # date account was activated after mail was sent.
    free_subscription_ends_on   = models.DateTimeField(blank=True,null=True) # set 1 month of site use,like its done on medium.com
 
    # is_subscriber     = models.BooleanField(default=False) # for payed users.

    def __str__(self):
        return self.username


    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return self.last_name +' '+self.first_name
        return self.username

    @property
    def user_username(self):
        return "{0}@inQ".format(str(self.username))


    @property
    def questions_count(self):
        return self.questions.count


    @property
    def free_subscription_ended(self):
        if not self.free_subscription_ends_on is None:
            return bool(self.free_subscription_ends_on < timezone.now())


    def get_absolute_url(self):
        return reverse('users:user-view',args=[str(self.username)])


    @property
    def url(self):
        # i kind of like shortcuts :)
        return self.get_absolute_url()


    @property
    def people_user_is_connected_to(self):
        return [connection.from_user for connection in self.from_user.all()]


    @property
    def people_connected_to_count(self):
        # returns a count of all the people i have connected to,but not connected to me.
        # users connected to us are not regarded as a connection. (just wants things that way.)
        return self.to_user.count()
    



    
    
    
class Profile(models.Model):
    '''
    user profile.
    @attr
    +owner
    +profession
    +pic
    +bio


    '''
    owner           = models.OneToOneField(to=settings.AUTH_USER_MODEL,
                                            related_name='profile',
                                            on_delete=models.CASCADE)
    pic             = models.ImageField(upload_to=helpers.dp_upload_loc,blank=True,null=True)
    bio             = models.TextField(max_length=150,blank=True,null=True,default='This project was built as my #2 exercise with Python.')
    profession      = models.CharField(max_length=150,blank=True,null=True)
    gender          = models.CharField(max_length=6,blank=True,null=True)

    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    class Meta:
        ordering       = ('-created',)
        verbose_name   = 'Profile'
        verbose_name_plural = 'Profiles'


    def __str__(self):
        return str(self.owner.username)



    @property
    def pic_url(self):
        if self.pic:
            return self.pic.url
        return
    






class Activation(models.Model):
    ''' Activation Model.'''
    token       = models.CharField(max_length=250,unique=True,blank=True,null=True)
    user        = models.ForeignKey(to=User,on_delete=models.CASCADE)
    expired     = models.DateTimeField(blank=True,null=True)
    is_sent     = models.BooleanField(default=False)

    created     = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Activation'
        verbose_name_plural = 'Activations'


    def __str__(self):
        return '{0}'.format(self.token)



    @classmethod
    def create_activation_token(cls,user):
        # creates and returns activation object
        return cls.objects.create(token=activation_token(),
                                  user=user,
                                  expired=date_expired(),
                                  is_sent=True)


    def send(self,request = None):
        '''@method - send activation email'''
        if request is not None:
            domain = get_current_site(request).domain

            # get activation route full path.
            full_activation_url = build_absolute_uri(
                reverse(
                    'account:validate-token',
                    kwargs={'token':self.token}
                ),
                request
            )
            # print(full_activation_url)
            subject = 'Account Activation Confirmation.'
            message = "To activate {0} account for email {1} click on this link {2}".format(domain,
                self.user.email,
                full_activation_url)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = self.user.email

            try:
                send_mail(subject,message,from_email,[to_email],fail_silently=True)
                # print('mail sent')
            except BadHeaderError:
                pass



    def is_expired(self):
        return self.expired < timezone.now()




