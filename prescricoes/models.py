from django.db import models
from consultas.models import Consulta
from medicos.models import Medico
from pacientes.models import Paciente


class Prescricao(models.Model):
    consulta = models.ForeignKey(
        Consulta, on_delete=models.PROTECT, related_name="prescricoes"
    )
    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, related_name="prescricoes"
    )
    medico = models.ForeignKey(
        Medico, on_delete=models.PROTECT, related_name="prescricoes"
    )
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Prescrição — {self.paciente}"


class ItemPrescricao(models.Model):
    prescricao = models.ForeignKey(
        Prescricao, on_delete=models.CASCADE, related_name="itens"
    )
    medicamento = models.CharField(max_length=150)
    dosagem = models.CharField(max_length=100)
    frequencia = models.CharField(max_length=100)
    duracao = models.CharField(max_length=100)
    orientacoes = models.TextField(blank=True)
