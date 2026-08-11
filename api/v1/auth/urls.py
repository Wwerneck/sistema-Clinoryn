from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import ClinorynTokenObtainPairView, MeView


app_name = "auth"

urlpatterns = [
    path("login/", ClinorynTokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("me/", MeView.as_view(), name="me"),
]
