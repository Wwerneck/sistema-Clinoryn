from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class RecepcaoPermissionTests(TestCase):
    def test_reception_management_is_admin_only(self):
        receptionist = User.objects.create_user(username="recep", password="test", role=User.Role.RECEPCAO)
        self.client.force_login(receptionist)
        self.assertEqual(self.client.get(reverse("recepcao:list")).status_code, 403)
        self.assertEqual(self.client.get(reverse("recepcao:create")).status_code, 403)

    def test_reception_can_access_operational_dashboard(self):
        receptionist = User.objects.create_user(username="operacional", password="test", role=User.Role.RECEPCAO)
        self.client.force_login(receptionist)
        self.assertEqual(self.client.get(reverse("recepcao:dashboard")).status_code, 200)
        self.assertEqual(self.client.get(reverse("recepcao:daily-schedule")).status_code, 200)

    def test_patient_cannot_access_reception_dashboard(self):
        patient = User.objects.create_user(username="outside", password="test", role=User.Role.PACIENTE)
        self.client.force_login(patient)
        self.assertEqual(self.client.get(reverse("recepcao:dashboard")).status_code, 403)
