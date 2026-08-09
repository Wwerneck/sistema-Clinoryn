from django.urls import path

from .views import UserLoginView, UserLogoutView

app_name = "accounts"
urlpatterns = [
    path("entrar/", UserLoginView.as_view(), name="login"),
    path("sair/", UserLogoutView.as_view(), name="logout"),
]
