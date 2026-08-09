from django.core.exceptions import ValidationError
from django.db import models

from consultas.models import Consulta
from medicos.models import Medico
from pacientes.models import Paciente


class Prontuario(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.PROTECT, related_name="prontuario")
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name="prontuarios")
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT, related_name="prontuarios")
    queixa_principal = models.TextField()
    sintomas = models.TextField(blank=True)
    historico = models.TextField(blank=True)
    alergias = models.TextField(blank=True)
    antecedentes = models.TextField(blank=True)
    doencas_preexistentes = models.TextField(blank=True)
    medicamentos_em_uso = models.TextField(blank=True)
    historico_familiar = models.TextField(blank=True)
    diagnostico = models.TextField(blank=True)
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-consulta__data", "-consulta__hora_inicio")

    def clean(self):
        if self.consulta_id and (self.paciente_id != self.consulta.paciente_id or self.medico_id != self.consulta.medico_id):
            raise ValidationError("Paciente e médico devem corresponder à consulta.")

    def __str__(self):
        return f"Prontuário de {self.paciente} — {self.consulta.data:%d/%m/%Y}"


class EvolucaoClinica(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name="evolucoes")
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT, related_name="evolucoes")
    descricao = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Evolução em {self.created_at:%d/%m/%Y %H:%M}"
