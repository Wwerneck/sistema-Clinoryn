from datetime import time, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from especialidades.models import Especialidade
from medicos.models import Medico
from pacientes.models import Paciente
from consultas.models import Consulta
from prontuarios.models import Prontuario
from exames.models import Exame
from financeiro.models import Pagamento


class MedicalAreaTests(TestCase):
    def setUp(self):
        specialty = Especialidade.objects.get(nome="Pediatria")
        self.users, self.doctors = [], []
        for index in range(2):
            user = User.objects.create_user(
                username=f"med-area-{index}", role=User.Role.MEDICO
            )
            doctor = Medico.objects.create(
                user=user,
                nome=f"Médico {index}",
                crm=f"CRM {index}",
                especialidade=specialty,
                telefone="1",
                email=f"m{index}@e.com",
                valor_consulta=100,
                duracao_consulta=30,
            )
            self.users.append(user)
            self.doctors.append(doctor)
        patient_user = User.objects.create_user(
            username="patient-area", role=User.Role.PACIENTE
        )
        self.patient = Paciente.objects.create(
            user=patient_user,
            nome_completo="Paciente Teste",
            cpf="52998224725",
            data_nascimento="1990-01-01",
            sexo="N",
            telefone="1",
            email="p@e.com",
            endereco="Rua",
            numero="1",
            bairro="Centro",
            cidade="SP",
            estado="SP",
            cep="01001000",
        )
        self.appointment = Consulta.objects.create(
            paciente=self.patient,
            medico=self.doctors[0],
            especialidade=specialty,
            data=timezone.localdate() + timedelta(days=1),
            hora_inicio=time(9),
            hora_fim=time(9, 30),
            valor=100,
            status=Consulta.Status.AGUARDANDO,
            created_by=self.users[0],
            updated_by=self.users[0],
        )

    def test_doctor_dashboard_requires_medical_profile(self):
        self.client.force_login(self.users[0])
        self.assertEqual(self.client.get(reverse("medicos:dashboard")).status_code, 200)

    def test_doctor_cannot_change_another_doctors_appointment(self):
        self.client.force_login(self.users[1])
        response = self.client.post(
            reverse(
                "medicos:attendance-status",
                args=(self.appointment.pk, Consulta.Status.EM_ATENDIMENTO),
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_doctor_can_start_and_finish_own_appointment(self):
        self.client.force_login(self.users[0])
        self.client.post(
            reverse(
                "medicos:attendance-status",
                args=(self.appointment.pk, Consulta.Status.EM_ATENDIMENTO),
            )
        )
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, Consulta.Status.EM_ATENDIMENTO)
        self.client.post(
            reverse(
                "medicos:attendance-status",
                args=(self.appointment.pk, Consulta.Status.CONCLUIDA),
            )
        )
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, Consulta.Status.CONCLUIDA)

    def test_reception_cannot_access_medical_dashboard(self):
        user = User.objects.create_user(
            username="reception-area", role=User.Role.RECEPCAO
        )
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("medicos:dashboard")).status_code, 403)

    def test_reception_cannot_access_medical_record(self):
        user = User.objects.create_user(
            username="reception-record", role=User.Role.RECEPCAO
        )
        self.client.force_login(user)
        self.assertEqual(
            self.client.get(
                reverse("prontuarios:record", args=(self.appointment.pk,))
            ).status_code,
            403,
        )

    def test_doctor_cannot_open_another_doctors_record(self):
        self.client.force_login(self.users[1])
        self.assertEqual(
            self.client.get(
                reverse("prontuarios:record", args=(self.appointment.pk,))
            ).status_code,
            404,
        )

    def test_attending_doctor_can_create_record(self):
        self.client.force_login(self.users[0])
        response = self.client.post(
            reverse("prontuarios:record", args=(self.appointment.pk,)),
            {
                "queixa_principal": "Dor de cabeça",
                "sintomas": "Náusea",
                "historico": "",
                "alergias": "",
                "antecedentes": "",
                "doencas_preexistentes": "",
                "medicamentos_em_uso": "",
                "historico_familiar": "",
                "diagnostico": "Cefaleia",
                "observacoes": "",
            },
        )
        self.assertRedirects(
            response, reverse("prontuarios:record", args=(self.appointment.pk,))
        )
        record = Prontuario.objects.get(consulta=self.appointment)
        self.assertEqual(record.medico, self.doctors[0])
        self.assertEqual(record.paciente, self.patient)

    def test_other_doctor_cannot_download_exam(self):
        exam = Exame.objects.create(
            paciente=self.patient,
            medico=self.doctors[0],
            consulta=self.appointment,
            tipo_exame="Hemograma",
            arquivo="private/exames/test.pdf",
        )
        self.client.force_login(self.users[1])
        self.assertEqual(
            self.client.get(reverse("exames:download", args=(exam.pk,))).status_code,
            404,
        )

    def test_reception_cannot_list_exams_or_prescriptions(self):
        user = User.objects.create_user(
            username="reception-documents", role=User.Role.RECEPCAO
        )
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("exames:list")).status_code, 403)
        self.assertEqual(self.client.get(reverse("prescricoes:list")).status_code, 403)

    def test_doctor_financial_dashboard_hides_other_doctors_values(self):
        Pagamento.objects.create(
            consulta=self.appointment,
            paciente=self.patient,
            medico=self.doctors[0],
            valor=100,
            forma_pagamento="PIX",
            status="PAGO",
            registrado_por=self.users[0],
        )
        other = Consulta.objects.create(
            paciente=self.patient,
            medico=self.doctors[1],
            especialidade=self.doctors[1].especialidade,
            data=timezone.localdate() + timedelta(days=2),
            hora_inicio=time(10),
            hora_fim=time(10, 30),
            valor=999,
            created_by=self.users[1],
            updated_by=self.users[1],
        )
        Pagamento.objects.create(
            consulta=other,
            paciente=self.patient,
            medico=self.doctors[1],
            valor=999,
            forma_pagamento="PIX",
            status="PAGO",
            registrado_por=self.users[1],
        )
        self.client.force_login(self.users[0])
        response = self.client.get(reverse("financeiro:dashboard"))
        self.assertContains(response, "100,00")
        self.assertNotContains(response, "999,00")

    def test_doctor_cannot_register_payment(self):
        self.client.force_login(self.users[0])
        self.assertEqual(
            self.client.get(
                reverse("financeiro:register", args=(self.appointment.pk,))
            ).status_code,
            403,
        )
