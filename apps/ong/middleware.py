from django.shortcuts import render

from .permissions import user_has_cms_access


PROTECTED_PREFIXES = ("/admin/", "/ckeditor5/")


class AdminGroupRequiredMiddleware:
    """Limit CMS/admin surfaces to staff users in the expected groups."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._is_protected_path(request.path_info) and request.user.is_authenticated:
            if not user_has_cms_access(request.user):
                return render(request, "403.html", status=403)
        return self.get_response(request)

    def _is_protected_path(self, path):
        return any(path.startswith(prefix) for prefix in PROTECTED_PREFIXES)
