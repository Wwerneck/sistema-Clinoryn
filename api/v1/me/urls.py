from django.urls import path

from .views import (
    MeConsultasView,
    MeExamesView,
    MePagamentosView,
    MePrescricoesView,
    MeProfileView,
)


app_name = "me"

urlpatterns = [
    path("", MeProfileView.as_view(), name="profile"),
    path("consultas/", MeConsultasView.as_view(), name="consultas"),
    path("exames/", MeExamesView.as_view(), name="exames"),
    path("prescricoes/", MePrescricoesView.as_view(), name="prescricoes"),
    path("pagamentos/", MePagamentosView.as_view(), name="pagamentos"),
]
