from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse


class DemoReadOnlyMiddleware:
    """Impede alterações persistentes quando a aplicação está em modo demonstrativo."""

    unsafe_methods = {"POST", "PUT", "PATCH", "DELETE"}
    allowed_paths = {"/conta/entrar/", "/conta/sair/"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._must_block(request):
            detail = (
                "Esta é uma demonstração em modo somente leitura. "
                "Ações de criação, edição e exclusão estão desativadas."
            )
            if request.path.startswith("/api/") or "application/json" in request.headers.get("Accept", ""):
                return JsonResponse({"detail": detail}, status=403)
            return HttpResponseForbidden(detail)
        return self.get_response(request)

    def _must_block(self, request):
        return (
            settings.DEMO_MODE
            and request.method in self.unsafe_methods
            and request.path not in self.allowed_paths
        )
