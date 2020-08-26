from re import compile
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from utils import timing_is_valid

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/')), compile('password')]


if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
	EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(MiddlewareMixin):
	"""Middleware that requires a user to be authenticated to view any page other 
	than LOGIN_URL. Exemptions to this requirement can be optionally specified
	in settings via a list of regular expressions in LOGIN_EXEMPT_URLS.

	Requires authentication middleware and template context processors to 
	be loaded."""

	def process_request(self, request):
		assert hasattr(request, 'user')
		if not request.user.is_authenticated:
			path = request.path_info.lstrip('/')
			if (not any(m.match(path) for m in EXEMPT_URLS)):
				return HttpResponseRedirect(settings.LOGIN_URL)



class ValidTimingRequiredMiddleware(MiddlewareMixin):
	"""Middleware that requires system timing to be set and valid to view any
	page that requires authentication. Otherwise, it redirects to the 
	system's process and timing page"""

	def process_request(self, request):
		path = request.path_info.lstrip('/')
		exemptions = ['timing', 'timing/update', 'login', 'logout']
		if not path in exemptions and not timing_is_valid():
			messages.info(request, "The Procurement Process and Timing has not yet been set!")
			return redirect('core:get_timing')