from datetime import date, time

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from api.tests.factories import create_medico, create_paciente, create_user
from consultas.models import Consulta
from exames.models import Exame
from prescricoes.models import ItemPrescricao, Prescricao
from prontuarios.models import Prontuario


class ClinicalApiTests(APITestCase):
    def setUp(self):
        self.admin = create_user(username="admin-clinical", role=User.Role.ADMIN)
        self.recepcao = create_user(username="recepcao-clinical", role=User.Role.RECEPCAO)
        self.patient = create_paciente(username="paciente_clinical", cpf="39053344705")
        self.other_patient = create_paciente(username="outro_clinical", cpf="11144477735")
        self.medico = create_medico(username="medico_clinical", crm="CRM-CLIN-1")
        self.other_medico = create_medico(username="outro_medico_clinical", crm="CRM-CLIN-2")
        self.consulta = self.create_consulta(self.patient, self.medico, time(9))
        self.other_consulta = self.create_consulta(self.other_patient, self.other_medico, time(10))

    def create_consulta(self, paciente, medico, start):
        return Consulta.objects.create(
            paciente=paciente,
            medico=medico,
            especialidade=medico.especialidade,
            data=date(2030, 1, 1),
            hora_inicio=start,
            hora_fim=time(start.hour, 30),
            valor=medico.valor_consulta,
            created_by=self.admin,
            updated_by=self.admin,
        )

    def test_reception_cannot_list_clinical_records(self):
        self.client.force_authenticate(self.recepcao)

        response = self.client.get(reverse("api-v1:prontuario-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_patient_cannot_access_prontuario(self):
        Prontuario.objects.create(
            consulta=self.consulta,
            paciente=self.patient,
            medico=self.medico,
            queixa_principal="Dor",
        )
        self.client.force_authenticate(self.patient.user)

        response = self.client.get(reverse("api-v1:prontuario-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_doctor_cannot_create_prontuario_for_other_doctor_consulta(self):
        self.client.force_authenticate(self.medico.user)

        response = self.client.post(
            reverse("api-v1:prontuario-list"),
            {"consulta": self.other_consulta.id, "queixa_principal": "Dor"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_only_lists_own_prescriptions(self):
        own = Prescricao.objects.create(consulta=self.consulta, paciente=self.patient, medico=self.medico)
        ItemPrescricao.objects.create(
            prescricao=own,
            medicamento="A",
            dosagem="1",
            frequencia="1x",
            duracao="1 dia",
        )
        other = Prescricao.objects.create(
            consulta=self.other_consulta,
            paciente=self.other_patient,
            medico=self.other_medico,
        )
        ItemPrescricao.objects.create(
            prescricao=other,
            medicamento="B",
            dosagem="1",
            frequencia="1x",
            duracao="1 dia",
        )
        self.client.force_authenticate(self.patient.user)

        listed = self.client.get(reverse("api-v1:prescricao-list"))
        detail_other = self.client.get(reverse("api-v1:prescricao-detail", args=[other.id]))

        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertEqual(listed.data["count"], 1)
        self.assertEqual(listed.data["results"][0]["id"], own.id)
        self.assertEqual(detail_other.status_code, status.HTTP_404_NOT_FOUND)

    def test_patient_cannot_create_prescription(self):
        self.client.force_authenticate(self.patient.user)

        response = self.client.post(
            reverse("api-v1:prescricao-list"),
            {
                "consulta": self.consulta.id,
                "observacoes": "",
                "itens": [{"medicamento": "A", "dosagem": "1", "frequencia": "1x", "duracao": "1 dia"}],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patient_cannot_access_other_patient_exam_file(self):
        exam = Exame.objects.create(
            consulta=self.other_consulta,
            paciente=self.other_patient,
            medico=self.other_medico,
            tipo_exame="Hemograma",
            arquivo=SimpleUploadedFile("resultado.pdf", b"%PDF-1.4", content_type="application/pdf"),
        )
        self.client.force_authenticate(self.patient.user)

        detail = self.client.get(reverse("api-v1:exame-detail", args=[exam.id]))
        file_response = self.client.get(reverse("api-v1:exame-arquivo", args=[exam.id]))

        self.assertEqual(detail.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(file_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_exam_serializer_does_not_expose_storage_path(self):
        exam = Exame.objects.create(
            consulta=self.consulta,
            paciente=self.patient,
            medico=self.medico,
            tipo_exame="Raio X",
            arquivo=SimpleUploadedFile("resultado.pdf", b"%PDF-1.4", content_type="application/pdf"),
        )
        self.client.force_authenticate(self.patient.user)

        response = self.client.get(reverse("api-v1:exame-detail", args=[exam.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("arquivo", response.data)
        self.assertTrue(response.data["possui_arquivo"])
