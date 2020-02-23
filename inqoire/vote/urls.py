from django.urls import path
from .import views


app_name = 'vote'

urlpatterns = [
    path('user-vote/',views.vote,name='user-vote'),
]

