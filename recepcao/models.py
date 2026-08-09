from django.conf import settings
from django.db import models


class Recepcionista(models.Model):
    class Cargo(models.TextChoices):
        RECEPCIONISTA = "RECEPCIONISTA", "Recepcionista"
        SECRETARIA = "SECRETARIA", "Secretária"
        ATENDENTE = "ATENDENTE", "Atendente"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="recepcionista")
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20)
    cargo = models.CharField(max_length=15, choices=Cargo.choices)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("nome",)

    def __str__(self):
        return self.nome
