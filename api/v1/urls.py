from django.urls import include, path


app_name = "api-v1"

urlpatterns = [
    path("auth/", include("api.v1.auth.urls")),
    path("me/", include("api.v1.me.urls")),
    path("pacientes/", include("api.v1.pacientes.urls")),
    path("medicos/", include("api.v1.medicos.urls")),
    path("especialidades/", include("api.v1.especialidades.urls")),
    path("agenda/", include("api.v1.agenda.urls")),
    path("consultas/", include("api.v1.consultas.urls")),
    path("prontuarios/", include("api.v1.prontuarios.urls")),
    path("prescricoes/", include("api.v1.prescricoes.urls")),
    path("exames/", include("api.v1.exames.urls")),
    path("financeiro/", include("api.v1.financeiro.urls")),
]
