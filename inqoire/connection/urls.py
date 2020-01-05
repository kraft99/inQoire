from django.urls import path
from .import views


app_name = 'connection'

urlpatterns = [
    path('switch-connection/',views.switch_connection,name='connection-switch'),
]

