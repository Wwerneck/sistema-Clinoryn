from django.urls import path

from . import views

app_name = "dashboards"
urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/admin/", views.admin_dashboard, name="admin"),
    path("dashboard/medico/", views.medico_dashboard, name="medico"),
    path("dashboard/recepcao/", views.recepcao_dashboard, name="recepcao"),
    path("dashboard/paciente/", views.paciente_dashboard, name="paciente"),
]
