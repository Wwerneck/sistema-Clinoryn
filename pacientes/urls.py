from django.urls import path

from .views import PacienteCreateView, PacienteListView, patient_detail

app_name = "pacientes"
urlpatterns = [path("", PacienteListView.as_view(), name="list"), path("novo/", PacienteCreateView.as_view(), name="create"), path("<int:pk>/", patient_detail, name="detail")]
