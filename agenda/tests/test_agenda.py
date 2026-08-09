from datetime import date, time

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from especialidades.models import Especialidade
from medicos.models import Medico

from agenda.models import BloqueioAgenda, DisponibilidadeMedico


class AgendaTestMixin:
    def create_doctor(self, username, crm):
        user = User.objects.create_user(username=username, password="test", role=User.Role.MEDICO)
        doctor = Medico.objects.create(
            user=user,
            nome=f"Dr. {username}",
            crm=crm,
            especialidade=self.specialty,
            telefone="11999999999",
            email=f"{username}@example.com",
            valor_consulta="300.00",
            duracao_consulta=30,
        )
        return user, doctor

    def setUp(self):
        self.specialty = Especialidade.objects.create(nome="Cardiologia")
        self.doctor_user, self.doctor = self.create_doctor("carlos", "CRM-SP 123")
        self.other_user, self.other_doctor = self.create_doctor("ana", "CRM-SP 456")
        self.admin = User.objects.create_user(username="admin-agenda", password="test", role=User.Role.ADMIN)
        self.reception = User.objects.create_user(username="recepcao-agenda", password="test", role=User.Role.RECEPCAO)


class AgendaRuleTests(AgendaTestMixin, TestCase):
    def test_overlapping_availability_is_rejected(self):
        DisponibilidadeMedico.objects.create(
            medico=self.doctor,
            dia_semana=DisponibilidadeMedico.DiaSemana.SEGUNDA,
            hora_inicio=time(8),
            hora_fim=time(12),
        )
        overlapping = DisponibilidadeMedico(
            medico=self.doctor,
            dia_semana=DisponibilidadeMedico.DiaSemana.SEGUNDA,
            hora_inicio=time(11),
            hora_fim=time(13),
        )
        with self.assertRaises(ValidationError):
            overlapping.full_clean()

    def test_adjacent_availability_is_allowed(self):
        DisponibilidadeMedico.objects.create(
            medico=self.doctor,
            dia_semana=DisponibilidadeMedico.DiaSemana.SEGUNDA,
            hora_inicio=time(8),
            hora_fim=time(12),
        )
        adjacent = DisponibilidadeMedico(
            medico=self.doctor,
            dia_semana=DisponibilidadeMedico.DiaSemana.SEGUNDA,
            hora_inicio=time(12),
            hora_fim=time(16),
        )
        adjacent.full_clean()

    def test_overlapping_blocks_are_rejected(self):
        BloqueioAgenda.objects.create(
            medico=self.doctor,
            data=date(2026, 9, 1),
            hora_inicio=time(9),
            hora_fim=time(10),
            motivo=BloqueioAgenda.Motivo.REUNIAO,
        )
        block = BloqueioAgenda(
            medico=self.doctor,
            data=date(2026, 9, 1),
            hora_inicio=time(9, 30),
            hora_fim=time(11),
            motivo=BloqueioAgenda.Motivo.COMPROMISSO,
        )
        with self.assertRaises(ValidationError):
            block.full_clean()


class AgendaPermissionTests(AgendaTestMixin, TestCase):
    def test_reception_can_view_but_cannot_change_agenda(self):
        self.client.force_login(self.reception)
        self.assertEqual(self.client.get(reverse("agenda:list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("agenda:availability-create")).status_code, 403)
        self.assertEqual(self.client.get(reverse("agenda:block-create")).status_code, 403)

    def test_doctor_cannot_create_availability_for_another_doctor(self):
        self.client.force_login(self.doctor_user)
        response = self.client.post(reverse("agenda:availability-create"), {
            "medico": self.other_doctor.pk,
            "dia_semana": DisponibilidadeMedico.DiaSemana.TERCA,
            "hora_inicio": "08:00",
            "hora_fim": "12:00",
            "duracao_consulta": 30,
            "ativo": True,
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(DisponibilidadeMedico.objects.exists())

    def test_doctor_sees_only_own_agenda(self):
        DisponibilidadeMedico.objects.create(medico=self.doctor, dia_semana=0, hora_inicio=time(8), hora_fim=time(12))
        DisponibilidadeMedico.objects.create(medico=self.other_doctor, dia_semana=0, hora_inicio=time(8), hora_fim=time(12))
        self.client.force_login(self.doctor_user)
        response = self.client.get(reverse("agenda:list"))
        self.assertContains(response, self.doctor.nome)
        self.assertNotContains(response, self.other_doctor.nome)

    def test_admin_can_create_availability(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse("agenda:availability-create"), {
            "medico": self.doctor.pk,
            "dia_semana": DisponibilidadeMedico.DiaSemana.QUARTA,
            "hora_inicio": "08:00",
            "hora_fim": "12:00",
            "duracao_consulta": 30,
            "ativo": True,
        })
        self.assertRedirects(response, reverse("agenda:list"))
        self.assertEqual(DisponibilidadeMedico.objects.count(), 1)
