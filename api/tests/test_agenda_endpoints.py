from datetime import time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from agenda.models import DisponibilidadeMedico
from api.tests.factories import create_medico, create_user


class AgendaApiTests(APITestCase):
    def setUp(self):
        self.admin = create_user(username="admin-agenda-api", role=User.Role.ADMIN)
        self.recepcao = create_user(username="recepcao-agenda-api", role=User.Role.RECEPCAO)
        self.medico = create_medico(username="medico_agenda_api", crm="CRM-AGENDA-1")
        self.other_medico = create_medico(username="outro_medico_api", crm="CRM-AGENDA-2")

    def test_reception_can_read_but_not_create_availability(self):
        DisponibilidadeMedico.objects.create(
            medico=self.medico,
            dia_semana=0,
            hora_inicio=time(8),
            hora_fim=time(12),
        )
        self.client.force_authenticate(self.recepcao)

        listed = self.client.get(reverse("api-v1:agenda-disponibilidade-list"))
        created = self.client.post(
            reverse("api-v1:agenda-disponibilidade-list"),
            {
                "medico": self.medico.id,
                "dia_semana": 1,
                "hora_inicio": "08:00",
                "hora_fim": "12:00",
                "duracao_consulta": 30,
                "ativo": True,
            },
            format="json",
        )

        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertEqual(created.status_code, status.HTTP_403_FORBIDDEN)

    def test_doctor_cannot_create_availability_for_another_doctor(self):
        self.client.force_authenticate(self.medico.user)

        response = self.client.post(
            reverse("api-v1:agenda-disponibilidade-list"),
            {
                "medico": self.other_medico.id,
                "dia_semana": 1,
                "hora_inicio": "08:00",
                "hora_fim": "12:00",
                "duracao_consulta": 30,
                "ativo": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_availability(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(
            reverse("api-v1:agenda-disponibilidade-list"),
            {
                "medico": self.medico.id,
                "dia_semana": 1,
                "hora_inicio": "08:00",
                "hora_fim": "12:00",
                "duracao_consulta": 30,
                "ativo": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
