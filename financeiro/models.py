from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from consultas.models import Consulta
from medicos.models import Medico
from pacientes.models import Paciente


class Pagamento(models.Model):
    class Forma(models.TextChoices):
        PIX = "PIX", "Pix"
        DINHEIRO = "DINHEIRO", "Dinheiro"
        CARTAO_CREDITO = "CARTAO_CREDITO", "Cartão de crédito"
        CARTAO_DEBITO = "CARTAO_DEBITO", "Cartão de débito"
        CONVENIO = "CONVENIO", "Convênio"
        OUTRO = "OUTRO", "Outro"

    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        PAGO = "PAGO", "Pago"
        CANCELADO = "CANCELADO", "Cancelado"
        ESTORNADO = "ESTORNADO", "Estornado"

    consulta = models.OneToOneField(
        Consulta, on_delete=models.PROTECT, related_name="pagamento"
    )
    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, related_name="pagamentos"
    )
    medico = models.ForeignKey(
        Medico, on_delete=models.PROTECT, related_name="pagamentos"
    )
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    forma_pagamento = models.CharField(max_length=20, choices=Forma.choices)
    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.PENDENTE
    )
    data_pagamento = models.DateTimeField(null=True, blank=True)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pagamentos_registrados",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("medico", "status")),
            models.Index(fields=("paciente", "status")),
        ]
