from datetime import time, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from agenda.models import BloqueioAgenda, DisponibilidadeMedico
from especialidades.models import Especialidade
from medicos.models import Medico
from pacientes.models import Paciente

from consultas.models import Consulta
from consultas.services import cancel_appointment, save_appointment, transition_status


class AppointmentServiceTests(TestCase):
    def setUp(self):
        self.day = timezone.localdate() + timedelta(days=7)
        specialty = Especialidade.objects.create(nome="Clínica Geral")
        doctor_user = User.objects.create_user(username="doctor-service", role=User.Role.MEDICO)
        self.doctor = Medico.objects.create(user=doctor_user, nome="Dra. Ana", crm="CRM 999", especialidade=specialty, telefone="1", email="ana@example.com", valor_consulta=200, duracao_consulta=30)
        DisponibilidadeMedico.objects.create(medico=self.doctor, dia_semana=self.day.weekday(), hora_inicio=time(8), hora_fim=time(12))
        self.actor = User.objects.create_user(username="admin-service", role=User.Role.ADMIN)
        self.patients = []
        for index in range(2):
            user = User.objects.create_user(username=f"patient-{index}", role=User.Role.PACIENTE)
            self.patients.append(Paciente.objects.create(user=user, nome_completo=f"Paciente {index}", cpf=("52998224725", "11144477735")[index], data_nascimento="1990-01-01", sexo="N", telefone="1", email=f"p{index}@e.com", endereco="Rua", numero="1", bairro="Centro", cidade="SP", estado="SP", cep="01001000"))

    def book(self, patient, at=time(9)):
        return save_appointment(paciente=patient, medico=self.doctor, data=self.day, hora_inicio=at, actor=self.actor)

    def test_doctor_conflict_is_rejected(self):
        self.book(self.patients[0])
        with self.assertRaises(ValidationError):
            self.book(self.patients[1])

    def test_patient_conflict_is_rejected(self):
        self.book(self.patients[0])
        with self.assertRaises(ValidationError):
            self.book(self.patients[0], time(9, 15))

    def test_blocked_time_is_rejected(self):
        BloqueioAgenda.objects.create(medico=self.doctor, data=self.day, hora_inicio=time(10), hora_fim=time(11), motivo="REUNIAO")
        with self.assertRaises(ValidationError):
            self.book(self.patients[0], time(10))

    def test_cancelled_appointment_releases_time(self):
        appointment = self.book(self.patients[0])
        cancel_appointment(appointment=appointment, actor=self.actor)
        replacement = self.book(self.patients[1])
        self.assertEqual(replacement.hora_inicio, time(9))

    def test_status_flow_rejects_arbitrary_jump(self):
        appointment = self.book(self.patients[0])
        with self.assertRaises(ValidationError):
            transition_status(appointment=appointment, new_status=Consulta.Status.CONCLUIDA, actor=self.actor)

    def test_valid_reception_flow(self):
        appointment = self.book(self.patients[0])
        for status in (Consulta.Status.CONFIRMADA, Consulta.Status.PACIENTE_CHEGOU, Consulta.Status.AGUARDANDO):
            appointment = transition_status(appointment=appointment, new_status=status, actor=self.actor)
        self.assertEqual(appointment.status, Consulta.Status.AGUARDANDO)
