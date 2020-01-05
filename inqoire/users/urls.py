
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
	path('inQ/<str:username>/',views.view_by_user,name='user-view'),
    
]
