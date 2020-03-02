from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.http import Http404

from inqoire.users import models
from inqoire.utils.ip import visitor_ip_address




class RestrictUserToAdminRouteMiddleware(MiddlewareMixin):
	# restrict unathorized users access to admin route.
    def process_request(self,request):
        if not hasattr(request,'user'):
            raise ImproperlyConfigured(
                "django.contrib.auth.middleware.AuthenticationMiddleware middleware must come "
                "before account.middlewares.ActiveUserMiddleware."
            )

        if request.path.startswith('/admin'):
        	if request.user.is_authenticated:
        		if not (request.user.is_superuser or request.user.is_staff):
        			raise Http404()
        		else:
        			return
        	else:
        		raise Http404()
        


class LastIPMiddleware(MiddlewareMixin):
    # This middleware retrieves and sets user ip address 
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        # retrieve ip from request
        last_ip = visitor_ip_address(request)

        if request.user.last_seen_ip == last_ip:
            return

        # set new ip for user
        (models.User._default_manager
            .filter(pk=request.user.pk)
            .update(last_seen_ip=last_ip))



# class ActiveUserMiddleware(MiddlewareMixin):
#     # redundant as @login_required does the same
#     # middle saves user from repeating decorators on views.
#     def process_request(self, request):
#         if not request.user.is_authenticated:
#             return

#         if not request.user.is_active:
#             logout(request)
