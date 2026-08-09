from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .services import log_action


@receiver(user_logged_in)
def audit_login(sender, request, user, **kwargs):
    log_action(action="LOGIN", user=user)


@receiver(user_logged_out)
def audit_logout(sender, request, user, **kwargs):
    log_action(action="LOGOUT", user=user)
