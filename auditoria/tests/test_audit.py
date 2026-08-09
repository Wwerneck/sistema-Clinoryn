from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from auditoria.models import AuditLog


class AuditTests(TestCase):
    def test_login_is_audited_with_request_context(self):
        user = User.objects.create_user(username="audit-user", password="StrongPass123!", role=User.Role.ADMIN)
        self.client.post(reverse("accounts:login"), {"username": user.username, "password": "StrongPass123!"}, REMOTE_ADDR="127.0.0.1", HTTP_USER_AGENT="Audit test")
        log = AuditLog.objects.get(acao="LOGIN")
        self.assertEqual(log.user, user)
        self.assertEqual(str(log.ip_address), "127.0.0.1")
        self.assertEqual(log.user_agent, "Audit test")

    def test_audit_screen_is_admin_only(self):
        admin = User.objects.create_user(username="audit-admin", role=User.Role.ADMIN)
        reception = User.objects.create_user(username="audit-reception", role=User.Role.RECEPCAO)
        self.client.force_login(admin)
        self.assertEqual(self.client.get(reverse("auditoria:list")).status_code, 200)
        self.client.force_login(reception)
        self.assertEqual(self.client.get(reverse("auditoria:list")).status_code, 403)
