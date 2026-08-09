from datetime import date

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from pacientes.models import Paciente


class PacientePermissionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="test", role=User.Role.ADMIN)
        self.recepcao = User.objects.create_user(username="recepcao", password="test", role=User.Role.RECEPCAO)
        self.medico = User.objects.create_user(username="medico", password="test", role=User.Role.MEDICO)
        self.paciente = User.objects.create_user(username="paciente", password="test", role=User.Role.PACIENTE)

    def test_recepcao_can_open_patient_creation(self):
        self.client.force_login(self.recepcao)
        self.assertEqual(self.client.get(reverse("pacientes:create")).status_code, 200)

    def test_medico_cannot_create_patient(self):
        self.client.force_login(self.medico)
        self.assertEqual(self.client.get(reverse("pacientes:create")).status_code, 403)

    def test_patient_cannot_list_other_patients(self):
        self.client.force_login(self.paciente)
        self.assertEqual(self.client.get(reverse("pacientes:list")).status_code, 403)

    def test_creation_sets_role_and_hashes_password(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse("pacientes:create"), {
            "username": "maria",
            "password": "SenhaForte123!",
            "nome_completo": "Maria Silva",
            "cpf": "529.982.247-25",
            "data_nascimento": date(1990, 1, 1),
            "sexo": Paciente.Sexo.FEMININO,
            "telefone": "11999999999",
            "email": "maria@example.com",
            "endereco": "Rua das Flores",
            "numero": "10",
            "complemento": "",
            "bairro": "Centro",
            "cidade": "São Paulo",
            "estado": "SP",
            "cep": "01001000",
            "contato_emergencia": "José",
            "telefone_emergencia": "11888888888",
        })
        self.assertRedirects(response, reverse("pacientes:list"))
        profile = Paciente.objects.select_related("user").get(cpf="52998224725")
        self.assertEqual(profile.user.role, User.Role.PACIENTE)
        self.assertTrue(profile.user.check_password("SenhaForte123!"))
