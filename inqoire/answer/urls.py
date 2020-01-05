
from django.urls import path

from . import views

app_name = 'answer'

urlpatterns = [
	path('add/',views.answer_add,name='answer-add'),
	path('view/<str:slug>/',views.answer_view,name='answer-view'),
]
