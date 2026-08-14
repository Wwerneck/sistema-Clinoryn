from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import User


@override_settings(DEMO_MODE=True)
class DemoModeTests(TestCase):
    def test_blocks_unsafe_requests(self):
        response = self.client.post("/alteracao-demonstrativa/")

        self.assertEqual(response.status_code, 403)
        self.assertIn("somente leitura", response.content.decode())

    def test_allows_login_in_demo_mode(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "usuario-inexistente", "password": "SenhaInvalida123!"},
        )

        self.assertNotEqual(response.status_code, 403)


class DemoSeedCommandTests(TestCase):
    @override_settings(DEMO_MODE=False)
    def test_refuses_to_seed_without_demo_mode(self):
        with self.assertRaisesMessage(CommandError, "DEMO_MODE=True"):
            call_command("seed_demo")

    @override_settings(DEMO_MODE=True)
    def test_creates_demo_accounts_when_enabled(self):
        call_command("seed_demo")

        self.assertTrue(User.objects.filter(username="demo_admin", role=User.Role.ADMIN).exists())
        self.assertTrue(User.objects.filter(username="demo_medico", role=User.Role.MEDICO).exists())
