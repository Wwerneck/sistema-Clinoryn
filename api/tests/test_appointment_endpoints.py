from datetime import time, timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from agenda.models import DisponibilidadeMedico
from api.tests.factories import create_medico, create_paciente, create_user
from consultas.models import Consulta


class ConsultaApiTests(APITestCase):
    def setUp(self):
        self.day = timezone.localdate() + timedelta(days=10)
        self.admin = create_user(username="admin-consulta", role=User.Role.ADMIN)
        self.recepcao = create_user(username="recepcao-consulta", role=User.Role.RECEPCAO)
        self.patient = create_paciente(username="paciente_consulta", cpf="39053344705")
        self.other_patient = create_paciente(username="outro_paciente", cpf="11144477735")
        self.medico = create_medico(username="medico_consulta", crm="CRM-API-1")
        DisponibilidadeMedico.objects.create(
            medico=self.medico,
            dia_semana=self.day.weekday(),
            hora_inicio=time(8),
            hora_fim=time(12),
        )

    def payload(self, paciente=None, hora="09:00"):
        return {
            "paciente": paciente or self.patient.id,
            "medico": self.medico.id,
            "data": self.day.isoformat(),
            "hora_inicio": hora,
        }

    def test_reception_can_create_appointment_using_service_rules(self):
        self.client.force_authenticate(self.recepcao)

        response = self.client.post(reverse("api-v1:consulta-list"), self.payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["paciente"], self.patient.id)
        self.assertEqual(response.data["medico"], self.medico.id)
        self.assertEqual(response.data["status"], Consulta.Status.AGENDADA)

    def test_conflicting_appointment_is_rejected(self):
        self.client.force_authenticate(self.recepcao)
        first = self.client.post(reverse("api-v1:consulta-list"), self.payload(), format="json")
        second = self.client.post(
            reverse("api-v1:consulta-list"),
            self.payload(paciente=self.other_patient.id),
            format="json",
        )

        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(second.data["code"], "APPOINTMENT_INVALID")

    def test_patient_cannot_create_appointment_for_another_patient(self):
        self.client.force_authenticate(self.patient.user)

        response = self.client.post(
            reverse("api-v1:consulta-list"),
            self.payload(paciente=self.other_patient.id),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_status_transition_reuses_state_machine(self):
        self.client.force_authenticate(self.recepcao)
        created = self.client.post(reverse("api-v1:consulta-list"), self.payload(), format="json")

        invalid = self.client.post(reverse("api-v1:consulta-finalizar", args=[created.data["id"]]))
        valid = self.client.post(reverse("api-v1:consulta-confirmar", args=[created.data["id"]]))

        self.assertEqual(invalid.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(valid.status_code, status.HTTP_200_OK)
        self.assertEqual(valid.data["status"], Consulta.Status.CONFIRMADA)

    def test_patient_only_lists_own_appointments(self):
        Consulta.objects.create(
            paciente=self.patient,
            medico=self.medico,
            especialidade=self.medico.especialidade,
            data=self.day,
            hora_inicio=time(9),
            hora_fim=time(9, 30),
            valor=self.medico.valor_consulta,
            created_by=self.admin,
            updated_by=self.admin,
        )
        Consulta.objects.create(
            paciente=self.other_patient,
            medico=self.medico,
            especialidade=self.medico.especialidade,
            data=self.day,
            hora_inicio=time(10),
            hora_fim=time(10, 30),
            valor=self.medico.valor_consulta,
            created_by=self.admin,
            updated_by=self.admin,
        )
        self.client.force_authenticate(self.patient.user)

        response = self.client.get(reverse("api-v1:consulta-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["paciente"], self.patient.id)

    def test_available_slots_omits_booked_time(self):
        self.client.force_authenticate(self.recepcao)
        self.client.post(reverse("api-v1:consulta-list"), self.payload(), format="json")

        response = self.client.get(
            reverse("api-v1:consulta-horarios-disponiveis"),
            {"medico": self.medico.id, "data": self.day.isoformat()},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        starts = {item["hora_inicio"] for item in response.data["results"]}
        self.assertNotIn(time(9), starts)
        self.assertIn(time(8), starts)
