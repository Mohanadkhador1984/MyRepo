# backend/accounts/middleware.py

class CsrfExemptApiAuthMiddleware:
    """
    يستثني أي طلب يبدأ بالمسار /api/auth/ من تحقق CSRF.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/auth/"):
            request._dont_enforce_csrf_checks = True
        return self.get_response(request)
