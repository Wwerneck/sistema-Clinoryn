from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from especialidades.models import Especialidade


class Medico(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="medico")
    nome = models.CharField(max_length=150)
    crm = models.CharField(max_length=30, unique=True)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.PROTECT, related_name="medicos")
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    valor_consulta = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duracao_consulta = models.PositiveSmallIntegerField(default=30, validators=[MinValueValidator(5)])
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("nome",)
        indexes = [models.Index(fields=("nome",)), models.Index(fields=("crm",))]

    def save(self, *args, **kwargs):
        self.crm = self.crm.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} — {self.crm}"
