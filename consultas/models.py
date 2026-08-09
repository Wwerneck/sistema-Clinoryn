from django.conf import settings
from django.db import models
from django.db.models import F, Q

from especialidades.models import Especialidade
from medicos.models import Medico
from pacientes.models import Paciente


class Consulta(models.Model):
    class Status(models.TextChoices):
        AGENDADA = "AGENDADA", "Agendada"
        CONFIRMADA = "CONFIRMADA", "Confirmada"
        PACIENTE_CHEGOU = "PACIENTE_CHEGOU", "Paciente chegou"
        AGUARDANDO = "AGUARDANDO", "Aguardando"
        EM_ATENDIMENTO = "EM_ATENDIMENTO", "Em atendimento"
        CONCLUIDA = "CONCLUIDA", "Concluída"
        CANCELADA = "CANCELADA", "Cancelada"
        NAO_COMPARECEU = "NAO_COMPARECEU", "Não compareceu"

    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name="consultas")
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT, related_name="consultas")
    especialidade = models.ForeignKey(Especialidade, on_delete=models.PROTECT, related_name="consultas")
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AGENDADA)
    observacoes_administrativas = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="consultas_criadas")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="consultas_alteradas")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("data", "hora_inicio")
        constraints = [models.CheckConstraint(condition=Q(hora_fim__gt=F("hora_inicio")), name="consulta_horas_validas")]
        indexes = [models.Index(fields=("medico", "data", "status")), models.Index(fields=("paciente", "data", "status"))]

    def __str__(self):
        return f"{self.paciente} — {self.data:%d/%m/%Y} {self.hora_inicio:%H:%M}"
