from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q

from medicos.models import Medico


class DisponibilidadeMedico(models.Model):
    class DiaSemana(models.IntegerChoices):
        SEGUNDA = 0, "Segunda-feira"
        TERCA = 1, "Terça-feira"
        QUARTA = 2, "Quarta-feira"
        QUINTA = 3, "Quinta-feira"
        SEXTA = 4, "Sexta-feira"
        SABADO = 5, "Sábado"
        DOMINGO = 6, "Domingo"

    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="disponibilidades")
    dia_semana = models.PositiveSmallIntegerField(choices=DiaSemana.choices)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    duracao_consulta = models.PositiveSmallIntegerField(default=30, validators=[MinValueValidator(5)])
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("medico__nome", "dia_semana", "hora_inicio")
        constraints = [
            models.CheckConstraint(condition=Q(hora_fim__gt=F("hora_inicio")), name="agenda_disponibilidade_horas_validas"),
            models.UniqueConstraint(fields=("medico", "dia_semana", "hora_inicio", "hora_fim"), name="agenda_disponibilidade_periodo_unico"),
        ]
        indexes = [models.Index(fields=("medico", "dia_semana", "ativo"))]

    def clean(self):
        super().clean()
        if self.hora_inicio and self.hora_fim and self.hora_inicio >= self.hora_fim:
            raise ValidationError({"hora_fim": "O término deve ser posterior ao início."})
        if not self.medico_id or self.dia_semana is None or not self.hora_inicio or not self.hora_fim:
            return
        conflicts = type(self).objects.filter(
            medico_id=self.medico_id,
            dia_semana=self.dia_semana,
            ativo=True,
            hora_inicio__lt=self.hora_fim,
            hora_fim__gt=self.hora_inicio,
        ).exclude(pk=self.pk)
        if self.ativo and conflicts.exists():
            raise ValidationError("Este período se sobrepõe a outra disponibilidade ativa.")

    def __str__(self):
        return f"{self.medico} | {self.get_dia_semana_display()} {self.hora_inicio:%H:%M}–{self.hora_fim:%H:%M}"


class BloqueioAgenda(models.Model):
    class Motivo(models.TextChoices):
        FERIAS = "FERIAS", "Férias"
        FERIADO = "FERIADO", "Feriado"
        REUNIAO = "REUNIAO", "Reunião"
        COMPROMISSO = "COMPROMISSO", "Compromisso"
        INDISPONIBILIDADE = "INDISPONIBILIDADE", "Indisponibilidade"
        OUTRO = "OUTRO", "Outro"

    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="bloqueios")
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    motivo = models.CharField(max_length=20, choices=Motivo.choices)
    observacao = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-data", "hora_inicio")
        constraints = [
            models.CheckConstraint(condition=Q(hora_fim__gt=F("hora_inicio")), name="agenda_bloqueio_horas_validas"),
            models.UniqueConstraint(fields=("medico", "data", "hora_inicio", "hora_fim"), name="agenda_bloqueio_periodo_unico"),
        ]
        indexes = [models.Index(fields=("medico", "data"))]

    def clean(self):
        super().clean()
        if self.hora_inicio and self.hora_fim and self.hora_inicio >= self.hora_fim:
            raise ValidationError({"hora_fim": "O término deve ser posterior ao início."})
        if not self.medico_id or not self.data or not self.hora_inicio or not self.hora_fim:
            return
        conflicts = type(self).objects.filter(
            medico_id=self.medico_id,
            data=self.data,
            hora_inicio__lt=self.hora_fim,
            hora_fim__gt=self.hora_inicio,
        ).exclude(pk=self.pk)
        if conflicts.exists():
            raise ValidationError("Este período se sobrepõe a outro bloqueio.")

    def __str__(self):
        return f"{self.medico} | {self.data:%d/%m/%Y} {self.hora_inicio:%H:%M}–{self.hora_fim:%H:%M}"
