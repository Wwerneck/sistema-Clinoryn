from django.db import models
from consultas.models import Consulta
from medicos.models import Medico
from pacientes.models import Paciente
from .validators import validate_medical_file


class Exame(models.Model):
    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, related_name="exames"
    )
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT, related_name="exames")
    consulta = models.ForeignKey(
        Consulta, on_delete=models.PROTECT, related_name="exames"
    )
    tipo_exame = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    data_exame = models.DateField(null=True, blank=True)
    arquivo = models.FileField(
        upload_to="private/exames/%Y/%m/",
        validators=[validate_medical_file],
        null=True,
        blank=True,
    )
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
