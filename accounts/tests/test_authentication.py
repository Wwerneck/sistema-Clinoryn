from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class AuthenticationTests(TestCase):
    def test_login_redirects_each_role_to_its_dashboard(self):
        for role, route in (
            (User.Role.ADMIN, "dashboards:admin"),
            (User.Role.MEDICO, "dashboards:medico"),
            (User.Role.RECEPCAO, "dashboards:recepcao"),
            (User.Role.PACIENTE, "dashboards:paciente"),
        ):
            user = User.objects.create_user(username=role.lower(), password="StrongPass123!", role=role)
            self.client.force_login(user)
            response = self.client.get(reverse("dashboards:home"))
            self.assertRedirects(response, reverse(route))
            self.client.logout()

    def test_role_cannot_access_another_dashboard(self):
        user = User.objects.create_user(username="paciente", password="StrongPass123!", role=User.Role.PACIENTE)
        self.client.force_login(user)
        response = self.client.get(reverse("dashboards:medico"))
        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse("dashboards:paciente"))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('dashboards:paciente')}")

    def test_superuser_is_always_admin(self):
        user = User.objects.create_superuser(username="root", password="StrongPass123!")
        self.assertEqual(user.role, User.Role.ADMIN)
