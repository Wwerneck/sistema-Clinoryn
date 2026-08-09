from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginForm


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    pass
