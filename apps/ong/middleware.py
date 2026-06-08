from django.shortcuts import render


ADMIN_GROUPS = {"Admin", "Colaboradores"}
PROTECTED_PREFIXES = ("/admin/", "/ckeditor5/")


class AdminGroupRequiredMiddleware:
    """Limit CMS/admin surfaces to staff users in the expected groups."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._is_protected_path(request.path_info) and request.user.is_authenticated:
            if not self._has_cms_access(request.user):
                return render(request, "403.html", status=403)
        return self.get_response(request)

    def _is_protected_path(self, path):
        return any(path.startswith(prefix) for prefix in PROTECTED_PREFIXES)

    def _has_cms_access(self, user):
        if not user.is_active or not user.is_staff:
            return False
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=ADMIN_GROUPS).exists()
