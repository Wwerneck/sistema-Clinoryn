from django.urls import path

from .views import RecepcionistaCreateView, RecepcionistaListView, daily_schedule, operational_dashboard, update_appointment_status

app_name = "recepcao"
urlpatterns = [
    path("", RecepcionistaListView.as_view(), name="list"), path("novo/", RecepcionistaCreateView.as_view(), name="create"),
    path("dashboard/", operational_dashboard, name="dashboard"), path("agenda-diaria/", daily_schedule, name="daily-schedule"),
    path("consultas/<int:pk>/status/<str:status>/", update_appointment_status, name="appointment-status"),
]
