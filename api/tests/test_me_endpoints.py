from datetime import date, time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from api.tests.factories import create_medico, create_paciente, create_user
from consultas.models import Consulta
from financeiro.models import Pagamento


class MeApiTests(APITestCase):
    def setUp(self):
        self.admin = create_user(username="admin-me", role=User.Role.ADMIN)
        self.patient = create_paciente(username="paciente_me", cpf="39053344705")
        self.medico = create_medico(username="medico_me", crm="CRM-ME-1")
        self.consulta = Consulta.objects.create(
            paciente=self.patient,
            medico=self.medico,
            especialidade=self.medico.especialidade,
            data=date(2030, 3, 1),
            hora_inicio=time(9),
            hora_fim=time(9, 30),
            valor=self.medico.valor_consulta,
            created_by=self.admin,
            updated_by=self.admin,
        )

    def test_me_profile_returns_authenticated_user(self):
        self.client.force_authenticate(self.patient.user)

        response = self.client.get(reverse("api-v1:me:profile"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], User.Role.PACIENTE)
        self.assertEqual(response.data["profile"]["id"], self.patient.id)

    def test_patient_me_consultas_uses_authenticated_patient(self):
        self.client.force_authenticate(self.patient.user)

        response = self.client.get(reverse("api-v1:me:consultas"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["paciente"], self.patient.id)

    def test_non_patient_cannot_use_patient_me_subresources(self):
        self.client.force_authenticate(self.medico.user)

        response = self.client.get(reverse("api-v1:me:consultas"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patient_me_pagamentos_uses_authenticated_patient(self):
        Pagamento.objects.create(
            consulta=self.consulta,
            paciente=self.patient,
            medico=self.medico,
            valor=self.consulta.valor,
            forma_pagamento=Pagamento.Forma.PIX,
            status=Pagamento.Status.PAGO,
            registrado_por=self.admin,
        )
        self.client.force_authenticate(self.patient.user)

        response = self.client.get(reverse("api-v1:me:pagamentos"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["paciente"], self.patient.id)
