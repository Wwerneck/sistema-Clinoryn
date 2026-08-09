from django.db.models import Count, Sum
from django.utils import timezone

from accounts.models import User
from consultas.models import Consulta
from especialidades.models import Especialidade
from financeiro.models import Pagamento
from medicos.models import Medico
from pacientes.models import Paciente
from recepcao.models import Recepcionista


def admin_dashboard_data():
    today = timezone.localdate()
    month = Consulta.objects.filter(data__year=today.year, data__month=today.month)
    specialties = list(
        Especialidade.objects.annotate(total=Count("consultas")).order_by(
            "-total", "nome"
        )[:5]
    )
    doctors = list(
        Medico.objects.select_related("especialidade")
        .annotate(total=Count("consultas"))
        .order_by("-total", "nome")[:5]
    )
    statuses = list(
        month.values("status").annotate(total=Count("id")).order_by("-total")
    )
    return {
        "today": today,
        "active_doctors": Medico.objects.filter(ativo=True).count(),
        "patients": Paciente.objects.count(),
        "staff": Recepcionista.objects.filter(ativo=True).count(),
        "today_appointments": Consulta.objects.filter(data=today).count(),
        "month_appointments": month.count(),
        "cancellations": month.filter(status=Consulta.Status.CANCELADA).count(),
        "revenue": Pagamento.objects.filter(
            status=Pagamento.Status.PAGO,
            data_pagamento__year=today.year,
            data_pagamento__month=today.month,
        ).aggregate(total=Sum("valor"))["total"]
        or 0,
        "top_specialties": specialties,
        "top_doctors": doctors,
        "statuses": statuses,
        "dashboard_charts": {
            "specialties": {
                "labels": [item.nome for item in specialties],
                "values": [item.total for item in specialties],
            },
            "statuses": {
                "labels": [Consulta.Status(item["status"]).label for item in statuses],
                "values": [item["total"] for item in statuses],
            },
        },
        "users": User.objects.count(),
    }


def patient_dashboard_data(*, patient):
    today = timezone.localdate()
    appointments = Consulta.objects.filter(paciente=patient).select_related(
        "medico", "especialidade"
    )
    future = (
        appointments.filter(data__gte=today)
        .exclude(status=Consulta.Status.CANCELADA)
        .order_by("data", "hora_inicio")
    )
    return {
        "patient": patient,
        "next_appointment": future.first(),
        "future_count": future.count(),
        "past_count": appointments.filter(data__lt=today).count(),
        "exams_count": patient.exames.count(),
        "prescriptions_count": patient.prescricoes.count(),
        "recent_appointments": appointments.order_by("-data", "-hora_inicio")[:5],
    }
