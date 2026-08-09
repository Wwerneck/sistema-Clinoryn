from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from especialidades.models import Especialidade
from medicos.models import Medico


class MedicoPermissionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="delete-admin", password="test")
        self.doctor_user = User.objects.create_user(username="doctor", password="test", role=User.Role.MEDICO)
        self.doctor = Medico.objects.create(
            user=self.doctor_user,
            nome="Médico Teste",
            crm="CRM-DELETE",
            especialidade=Especialidade.objects.create(nome="Clínica Geral"),
            telefone="1",
            email="doctor@example.com",
            valor_consulta=100,
        )

    def test_only_admin_can_open_doctor_creation(self):
        for role, expected in ((User.Role.ADMIN, 200), (User.Role.RECEPCAO, 403), (User.Role.PACIENTE, 403)):
            user = User.objects.create_user(username=role.lower(), password="test", role=role)
            self.client.force_login(user)
            self.assertEqual(self.client.get(reverse("medicos:create")).status_code, expected)
            self.client.logout()

    def test_patient_can_list_active_doctors(self):
        user = User.objects.create_user(username="patient", password="test", role=User.Role.PACIENTE)
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("medicos:list")).status_code, 200)

    def test_only_admin_can_open_doctor_deletion(self):
        url = reverse("medicos:delete", args=(self.doctor.pk,))
        for user, expected in ((self.admin, 200), (self.doctor_user, 403)):
            self.client.force_login(user)
            self.assertEqual(self.client.get(url).status_code, expected)

    def test_admin_deactivates_doctor_without_deleting_records(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse("medicos:delete", args=(self.doctor.pk,)))
        self.assertRedirects(response, reverse("medicos:list"))
        self.doctor.refresh_from_db()
        self.doctor_user.refresh_from_db()
        self.assertFalse(self.doctor.ativo)
        self.assertFalse(self.doctor_user.is_active)
        self.assertTrue(Medico.objects.filter(pk=self.doctor.pk).exists())
        self.assertTrue(User.objects.filter(pk=self.doctor_user.pk).exists())
