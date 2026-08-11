from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny, IsAuthenticated


def api_docs_permissions():
    return (IsAuthenticated,) if settings.API_DOCS_REQUIRE_AUTH else (AllowAny,)


class ApiDocsPermissionMixin:
    def get_permissions(self):
        return [permission() for permission in api_docs_permissions()]


class ClinorynSpectacularAPIView(ApiDocsPermissionMixin, SpectacularAPIView):
    pass


class ClinorynSwaggerView(ApiDocsPermissionMixin, SpectacularSwaggerView):
    pass


class ClinorynRedocView(ApiDocsPermissionMixin, SpectacularRedocView):
    pass
