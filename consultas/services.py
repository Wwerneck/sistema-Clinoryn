from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from agenda.models import BloqueioAgenda, DisponibilidadeMedico
from medicos.models import Medico
from pacientes.models import Paciente

from .models import Consulta

ACTIVE = [
    Consulta.Status.AGENDADA,
    Consulta.Status.CONFIRMADA,
    Consulta.Status.PACIENTE_CHEGOU,
    Consulta.Status.AGUARDANDO,
    Consulta.Status.EM_ATENDIMENTO,
]
VALID_TRANSITIONS = {
    Consulta.Status.AGENDADA: {
        Consulta.Status.CONFIRMADA,
        Consulta.Status.CANCELADA,
        Consulta.Status.NAO_COMPARECEU,
    },
    Consulta.Status.CONFIRMADA: {
        Consulta.Status.PACIENTE_CHEGOU,
        Consulta.Status.CANCELADA,
        Consulta.Status.NAO_COMPARECEU,
    },
    Consulta.Status.PACIENTE_CHEGOU: {Consulta.Status.AGUARDANDO},
    Consulta.Status.AGUARDANDO: {Consulta.Status.EM_ATENDIMENTO},
    Consulta.Status.EM_ATENDIMENTO: {Consulta.Status.CONCLUIDA},
}


@transaction.atomic
def save_appointment(
    *, paciente, medico, data, hora_inicio, actor, observacoes="", instance=None
):
    action = "CONSULTA_REAGENDADA" if instance and instance.pk else "CONSULTA_CRIADA"
    medico = Medico.objects.select_for_update().get(pk=medico.pk, ativo=True)
    paciente = Paciente.objects.select_for_update().get(pk=paciente.pk)
    start = timezone.make_aware(datetime.combine(data, hora_inicio))
    if start <= timezone.now():
        raise ValidationError("Não é possível agendar um horário passado.")
    duration = medico.duracao_consulta
    end = start + timedelta(minutes=duration)
    availability = DisponibilidadeMedico.objects.filter(
        medico=medico,
        dia_semana=data.weekday(),
        ativo=True,
        hora_inicio__lte=hora_inicio,
        hora_fim__gte=end.time(),
    ).exists()
    if not availability:
        raise ValidationError("O horário está fora da disponibilidade do médico.")
    if BloqueioAgenda.objects.filter(
        medico=medico, data=data, hora_inicio__lt=end.time(), hora_fim__gt=hora_inicio
    ).exists():
        raise ValidationError("O horário está bloqueado na agenda médica.")
    conflicts = Consulta.objects.filter(
        data=data,
        status__in=ACTIVE,
        hora_inicio__lt=end.time(),
        hora_fim__gt=hora_inicio,
    ).exclude(pk=getattr(instance, "pk", None))
    if conflicts.filter(medico=medico).exists():
        raise ValidationError("O médico já possui consulta nesse período.")
    if conflicts.filter(paciente=paciente).exists():
        raise ValidationError("O paciente já possui consulta nesse período.")
    appointment = instance or Consulta(created_by=actor)
    appointment.paciente, appointment.medico = paciente, medico
    appointment.especialidade, appointment.data = medico.especialidade, data
    appointment.hora_inicio, appointment.hora_fim = hora_inicio, end.time()
    appointment.valor, appointment.updated_by = medico.valor_consulta, actor
    appointment.observacoes_administrativas = observacoes
    appointment.full_clean()
    appointment.save()
    from auditoria.services import log_action

    log_action(
        action=action,
        user=actor,
        obj=appointment,
        metadata={"status": appointment.status},
    )
    return appointment


@transaction.atomic
def cancel_appointment(*, appointment, actor):
    appointment = Consulta.objects.select_for_update().get(pk=appointment.pk)
    if appointment.status in (Consulta.Status.CONCLUIDA, Consulta.Status.CANCELADA):
        raise ValidationError("Esta consulta não pode ser cancelada.")
    appointment.status, appointment.updated_by = Consulta.Status.CANCELADA, actor
    appointment.save(update_fields=("status", "updated_by", "updated_at"))
    from auditoria.services import log_action

    log_action(action="CONSULTA_CANCELADA", user=actor, obj=appointment)
    return appointment


@transaction.atomic
def transition_status(*, appointment, new_status, actor):
    appointment = Consulta.objects.select_for_update().get(pk=appointment.pk)
    if new_status not in VALID_TRANSITIONS.get(appointment.status, set()):
        raise ValidationError("Transição de status inválida para esta consulta.")
    appointment.status, appointment.updated_by = new_status, actor
    appointment.save(update_fields=("status", "updated_by", "updated_at"))
    from auditoria.services import log_action

    log_action(
        action="CONSULTA_STATUS_ALTERADO",
        user=actor,
        obj=appointment,
        metadata={"novo_status": new_status},
    )
    return appointment
