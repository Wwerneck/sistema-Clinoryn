from django.urls import path
from .views import dashboard, register_payment

app_name = "financeiro"
urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("consulta/<int:consulta_id>/registrar/", register_payment, name="register"),
]
