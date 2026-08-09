from django.urls import path

from .views import AgendaListView, BloqueioCreateView, BloqueioDeleteView, DisponibilidadeCreateView, DisponibilidadeDeleteView

app_name = "agenda"
urlpatterns = [
    path("", AgendaListView.as_view(), name="list"),
    path("disponibilidades/nova/", DisponibilidadeCreateView.as_view(), name="availability-create"),
    path("disponibilidades/<int:pk>/excluir/", DisponibilidadeDeleteView.as_view(), name="availability-delete"),
    path("bloqueios/novo/", BloqueioCreateView.as_view(), name="block-create"),
    path("bloqueios/<int:pk>/excluir/", BloqueioDeleteView.as_view(), name="block-delete"),
]
