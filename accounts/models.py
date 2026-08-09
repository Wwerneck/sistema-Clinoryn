from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        MEDICO = "MEDICO", "Médico"
        RECEPCAO = "RECEPCAO", "Recepção"
        PACIENTE = "PACIENTE", "Paciente"

    role = models.CharField("perfil", max_length=10, choices=Role.choices)

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)
