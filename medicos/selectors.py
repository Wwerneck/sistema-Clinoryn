from django.db.models import Sum
from django.utils import timezone

from consultas.models import Consulta


def doctor_appointments(*, medico):
    return Consulta.objects.filter(medico=medico).select_related("paciente", "especialidade")


def doctor_dashboard_data(*, medico):
    today = timezone.localdate()
    base = doctor_appointments(medico=medico)
    today_items = base.filter(data=today).order_by("hora_inicio")
    month_items = base.filter(data__year=today.year, data__month=today.month)
    return {
        "today": today,
        "appointments": today_items,
        "waiting": today_items.filter(status__in=(Consulta.Status.PACIENTE_CHEGOU, Consulta.Status.AGUARDANDO)),
        "next_appointments": base.filter(data__gte=today, status__in=(Consulta.Status.AGENDADA, Consulta.Status.CONFIRMADA)).order_by("data", "hora_inicio")[:5],
        "today_count": today_items.count(),
        "waiting_count": today_items.filter(status__in=(Consulta.Status.PACIENTE_CHEGOU, Consulta.Status.AGUARDANDO)).count(),
        "completed_count": today_items.filter(status=Consulta.Status.CONCLUIDA).count(),
        "month_count": month_items.filter(status=Consulta.Status.CONCLUIDA).count(),
        "estimated_revenue": month_items.filter(status=Consulta.Status.CONCLUIDA).aggregate(total=Sum("valor"))["total"] or 0,
    }
