from django.urls import path

from .views import MedicoCreateView, MedicoDeleteView, MedicoListView, medical_dashboard, own_schedule, update_attendance_status

app_name = "medicos"
urlpatterns = [
    path("", MedicoListView.as_view(), name="list"), path("novo/", MedicoCreateView.as_view(), name="create"),
    path("<int:pk>/excluir/", MedicoDeleteView.as_view(), name="delete"),
    path("dashboard/", medical_dashboard, name="dashboard"), path("minha-agenda/", own_schedule, name="own-schedule"),
    path("consultas/<int:pk>/status/<str:status>/", update_attendance_status, name="attendance-status"),
]
