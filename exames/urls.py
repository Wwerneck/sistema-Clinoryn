from django.urls import path
from .views import create_exam, download, list_exams

app_name = "exames"
urlpatterns = [
    path("", list_exams, name="list"),
    path("consulta/<int:consulta_id>/novo/", create_exam, name="create"),
    path("<int:pk>/download/", download, name="download"),
]
