from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from api.tests.factories import create_medico, create_paciente, create_user
from consultas.models import Consulta


class PacienteApiTests(APITestCase):
    def setUp(self):
        self.admin = create_user(username="admin", role=User.Role.ADMIN)
        self.recepcao = create_user(username="recepcao", role=User.Role.RECEPCAO)
        self.patient_a = create_paciente(username="paciente_a", nome="Paciente A", cpf="39053344705")
        self.patient_b = create_paciente(username="paciente_b", nome="Paciente B", cpf="11144477735")
        self.medico = create_medico()

    def test_patient_only_lists_own_profile(self):
        self.client.force_authenticate(self.patient_a.user)

        response = self.client.get(reverse("api-v1:paciente-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.patient_a.id)

    def test_patient_cannot_retrieve_another_patient_by_id(self):
        self.client.force_authenticate(self.patient_a.user)

        response = self.client.get(reverse("api-v1:paciente-detail", args=[self.patient_b.id]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_doctor_only_lists_linked_patients(self):
        Consulta.objects.create(
            paciente=self.patient_a,
            medico=self.medico,
            especialidade=self.medico.especialidade,
            data=date(2030, 1, 1),
            hora_inicio="10:00",
            hora_fim="10:30",
            valor=self.medico.valor_consulta,
            created_by=self.admin,
            updated_by=self.admin,
        )
        self.client.force_authenticate(self.medico.user)

        response = self.client.get(reverse("api-v1:paciente-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.patient_a.id)

    def test_reception_can_create_patient_without_setting_role(self):
        self.client.force_authenticate(self.recepcao)

        response = self.client.post(
            reverse("api-v1:paciente-list"),
            {
                "username": "novo_paciente",
                "password": "StrongPass123!",
                "nome_completo": "Novo Paciente",
                "cpf": "52998224725",
                "data_nascimento": "1995-05-10",
                "sexo": "N",
                "telefone": "11911112222",
                "email": "novo@example.com",
                "endereco": "Rua Nova",
                "numero": "1",
                "bairro": "Centro",
                "cidade": "São Paulo",
                "estado": "SP",
                "cep": "01001000",
                "role": "ADMIN",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nome_completo"], "Novo Paciente")
