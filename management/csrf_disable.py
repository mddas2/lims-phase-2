from django.conf import settings
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class DisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        csrf_cookie_secure = getattr(settings, 'CSRF_COOKIE_SECURE', True)
        if request.path == reverse('login') or request.path == reverse('logout'):
            setattr(settings, 'CSRF_COOKIE_SECURE', False)
        else:
            setattr(settings, 'CSRF_COOKIE_SECURE', csrf_cookie_secure)
