from django.conf import settings
from urllib.parse import urljoin
from django.utils.encoding import iri_to_uri
from django.contrib.sites.shortcuts import get_current_site



def build_absolute_uri(location,request):
    # type: (str) -> str
    host = get_current_site(request).domain
    protocol = "https" if settings.ENABLE_SSL else "http"
    current_uri = "%s://%s" % (protocol, host)
    location = urljoin(current_uri, location)
    return iri_to_uri(location)



def is_post(request):
	# checks POST request
	return request.method == 'POST'


def post_data(request):
	# form(request.POST)
	if is_post(request):
		return request.POST
	return None

