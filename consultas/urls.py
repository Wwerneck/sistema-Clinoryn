from django.urls import path

from .views import ConsultaCreateView, ConsultaListView, ConsultaUpdateView, cancel

app_name = "consultas"
urlpatterns = [path("", ConsultaListView.as_view(), name="list"), path("nova/", ConsultaCreateView.as_view(), name="create"), path("<int:pk>/reagendar/", ConsultaUpdateView.as_view(), name="update"), path("<int:pk>/cancelar/", cancel, name="cancel")]
