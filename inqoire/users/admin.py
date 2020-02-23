from django.contrib import admin
from .models import User,Profile,Activation


admin.site.register(User,
					list_display=[
					'score',
					'phone_number',
					'joined_from_ip',
					'last_seen_ip',
					'activated_on',
					'free_subscription_ends_on'
					])

admin.site.register(Profile)

admin.site.register(Activation)
