from django.conf import settings


class PermissionsPolicyMiddleware:
    """Adds the Permissions-Policy header (SEC-TLS-01) unless a view has set its own."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.headers.setdefault("Permissions-Policy", settings.PERMISSIONS_POLICY)
        return response
