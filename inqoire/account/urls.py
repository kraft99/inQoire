
from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
	path('auth/register/',views.register,name='register'),
    path('auth/login/',views.login,name='login'),
    path('auth/logout/',views.logout,name='logout'),
    path('auth/verify-user-activation-code/<str:token>/',views.validate_confirmation_token,name='validate-token'),
    path('user/confirmation-reminder/<str:email>/',views.confirm_via_email,name='confirmation-reminder'),
    
]
