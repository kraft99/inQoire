from django.urls import path
from .import views


app_name = 'comment'

urlpatterns = [
    path('add/',views.comment_post,name='comment-post'),
]

