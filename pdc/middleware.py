from django.contrib.redirects.middleware import RedirectFallbackMiddleware
from django.http import HttpResponseRedirect


class TemporaryRedirectMiddleware(RedirectFallbackMiddleware):
    """
    Middleware that service 302 temporary redirects rather than
    the default 301 permanent redirect.
    """
    response_redirect_class = HttpResponseRedirect
