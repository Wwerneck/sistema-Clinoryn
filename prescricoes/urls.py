from django.urls import path
from .views import create_prescription, list_prescriptions

app_name = "prescricoes"
urlpatterns = [
    path("", list_prescriptions, name="list"),
    path("consulta/<int:consulta_id>/nova/", create_prescription, name="create"),
]
