from django.urls import path
from .views import add_evolution, patient_history, record

app_name = "prontuarios"
urlpatterns = [path("consulta/<int:consulta_id>/", record, name="record"), path("consulta/<int:consulta_id>/evolucao/", add_evolution, name="evolution"), path("paciente/<int:paciente_id>/historico/", patient_history, name="history")]
