"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include
from django.views import defaults as default_views

from . import views

urlpatterns = [
    path('',views.welcome_to_inqoire,name='index'),
    path('account/',include('inqoire.account.urls',namespace='account')),
    path('comment/',include('inqoire.comment.urls',namespace='comment')),
    path('answer/',include('inqoire.answer.urls',namespace='answer')),
    path('question/',include('inqoire.question.urls',namespace='question')),
    path('users/',include('inqoire.users.urls',namespace='users')),
    path('vote/',include('inqoire.vote.urls',namespace='vote')),
    path('connection/',include('inqoire.connection.urls',namespace='connection')),
    path('admin/', admin.site.urls),# change url in production. `SECURITY` reasons.
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Test Dev. Error Pages
    urlpatterns += [
        path('400/', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        path('403/', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        path('404/', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        path('500/', default_views.server_error),
    ]