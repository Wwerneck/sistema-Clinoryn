from datetime import date, time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from api.tests.factories import create_medico, create_paciente, create_user
from consultas.models import Consulta
from financeiro.models import Pagamento


class FinancialApiTests(APITestCase):
    def setUp(self):
        self.admin = create_user(username="admin-fin", role=User.Role.ADMIN)
        self.recepcao = create_user(username="recepcao-fin", role=User.Role.RECEPCAO)
        self.patient = create_paciente(username="paciente_fin", cpf="39053344705")
        self.other_patient = create_paciente(username="outro_fin", cpf="11144477735")
        self.medico = create_medico(username="medico_fin", crm="CRM-FIN-1")
        self.other_medico = create_medico(username="outro_medico_fin", crm="CRM-FIN-2")
        self.consulta = self.create_consulta(self.patient, self.medico, time(9))
        self.other_consulta = self.create_consulta(self.other_patient, self.other_medico, time(10))

    def create_consulta(self, paciente, medico, start):
        return Consulta.objects.create(
            paciente=paciente,
            medico=medico,
            especialidade=medico.especialidade,
            data=date(2030, 2, 1),
            hora_inicio=start,
            hora_fim=time(start.hour, 30),
            valor=medico.valor_consulta,
            created_by=self.admin,
            updated_by=self.admin,
        )

    def test_reception_registers_payment_using_consulta_values(self):
        self.client.force_authenticate(self.recepcao)

        response = self.client.post(
            reverse("api-v1:pagamento-list"),
            {
                "consulta": self.consulta.id,
                "forma_pagamento": Pagamento.Forma.PIX,
                "status": Pagamento.Status.PAGO,
                "valor": "9999.00",
                "paciente": self.other_patient.id,
                "medico": self.other_medico.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["valor"], "200.00")
        self.assertEqual(response.data["paciente"], self.patient.id)
        self.assertEqual(response.data["medico"], self.medico.id)

    def test_patient_cannot_register_payment(self):
        self.client.force_authenticate(self.patient.user)

        response = self.client.post(
            reverse("api-v1:pagamento-list"),
            {
                "consulta": self.consulta.id,
                "forma_pagamento": Pagamento.Forma.PIX,
                "status": Pagamento.Status.PAGO,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patient_only_lists_own_payments(self):
        own = Pagamento.objects.create(
            consulta=self.consulta,
            paciente=self.patient,
            medico=self.medico,
            valor=self.consulta.valor,
            forma_pagamento=Pagamento.Forma.PIX,
            status=Pagamento.Status.PAGO,
            registrado_por=self.recepcao,
        )
        other = Pagamento.objects.create(
            consulta=self.other_consulta,
            paciente=self.other_patient,
            medico=self.other_medico,
            valor=self.other_consulta.valor,
            forma_pagamento=Pagamento.Forma.PIX,
            status=Pagamento.Status.PAGO,
            registrado_por=self.recepcao,
        )
        self.client.force_authenticate(self.patient.user)

        listed = self.client.get(reverse("api-v1:pagamento-list"))
        detail_other = self.client.get(reverse("api-v1:pagamento-detail", args=[other.id]))

        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertEqual(listed.data["count"], 1)
        self.assertEqual(listed.data["results"][0]["id"], own.id)
        self.assertEqual(detail_other.status_code, status.HTTP_404_NOT_FOUND)

    def test_summary_is_scoped_to_authenticated_user(self):
        Pagamento.objects.create(
            consulta=self.consulta,
            paciente=self.patient,
            medico=self.medico,
            valor=self.consulta.valor,
            forma_pagamento=Pagamento.Forma.PIX,
            status=Pagamento.Status.PAGO,
            registrado_por=self.recepcao,
        )
        Pagamento.objects.create(
            consulta=self.other_consulta,
            paciente=self.other_patient,
            medico=self.other_medico,
            valor=self.other_consulta.valor,
            forma_pagamento=Pagamento.Forma.PIX,
            status=Pagamento.Status.PAGO,
            registrado_por=self.recepcao,
        )
        self.client.force_authenticate(self.patient.user)

        response = self.client.get(reverse("api-v1:pagamento-resumo"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total"], 1)
        self.assertEqual(response.data["recebido"], "200.00")
