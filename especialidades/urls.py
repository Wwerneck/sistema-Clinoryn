from django.urls import path

from .views import EspecialidadeCreateView, EspecialidadeListView, EspecialidadeUpdateView

app_name = "especialidades"
urlpatterns = [
    path("", EspecialidadeListView.as_view(), name="list"),
    path("nova/", EspecialidadeCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", EspecialidadeUpdateView.as_view(), name="update"),
]
