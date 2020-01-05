
from django.urls import path

from . import views

app_name = 'question'

urlpatterns = [
	path('ask/',views.question_page,name='question-page'),
]
