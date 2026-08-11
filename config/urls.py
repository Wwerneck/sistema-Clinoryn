from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from api.schema import ClinorynRedocView, ClinorynSpectacularAPIView, ClinorynSwaggerView
from config.views import health_live, health_ready

urlpatterns = [
    path("health/live/", health_live, name="health-live"),
    path("health/ready/", health_ready, name="health-ready"),
    path("api/schema/", ClinorynSpectacularAPIView.as_view(), name="api-schema"),
    path("api/docs/", ClinorynSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
    path("api/redoc/", ClinorynRedocView.as_view(url_name="api-schema"), name="api-redoc"),
    path("api/", include("api.urls")),
    path("admin/", admin.site.urls),
    path("conta/", include("accounts.urls")),
    path("especialidades/", include("especialidades.urls")),
    path("pacientes/", include("pacientes.urls")),
    path("medicos/", include("medicos.urls")),
    path("recepcao/", include("recepcao.urls")),
    path("agenda/", include("agenda.urls")),
    path("consultas/", include("consultas.urls")),
    path("prontuarios/", include("prontuarios.urls")),
    path("prescricoes/", include("prescricoes.urls")),
    path("exames/", include("exames.urls")),
    path("financeiro/", include("financeiro.urls")),
    path("auditoria/", include("auditoria.urls")),
    path("", include("dashboards.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static", show_indexes=False)
