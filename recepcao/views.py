from datetime import date

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView

from accounts.models import User
from accounts.permissions import RolesRequiredMixin
from accounts.permissions import roles_required
from consultas.models import Consulta
from consultas.selectors import appointments_for_date
from consultas.services import transition_status
from medicos.models import Medico

from .forms import RecepcionistaCreateForm
from .models import Recepcionista


class RecepcionistaListView(RolesRequiredMixin, ListView):
    allowed_roles = (User.Role.ADMIN,)
    model = Recepcionista
    paginate_by = 20
    template_name = "recepcao/list.html"


class RecepcionistaCreateView(RolesRequiredMixin, CreateView):
    allowed_roles = (User.Role.ADMIN,)
    form_class = RecepcionistaCreateForm
    template_name = "shared/form.html"
    success_url = reverse_lazy("recepcao:list")
    extra_context = {"title": "Novo profissional da recepção"}


@roles_required(User.Role.RECEPCAO, User.Role.ADMIN)
def operational_dashboard(request):
    today = timezone.localdate()
    appointments = appointments_for_date(date=today)
    counts = appointments.aggregate(
        total=Count("id"),
        aguardando=Count(
            "id",
            filter=Q(
                status__in=(Consulta.Status.PACIENTE_CHEGOU, Consulta.Status.AGUARDANDO)
            ),
        ),
        confirmadas=Count("id", filter=Q(status=Consulta.Status.CONFIRMADA)),
        pendentes=Count("id", filter=Q(status=Consulta.Status.AGENDADA)),
        canceladas=Count("id", filter=Q(status=Consulta.Status.CANCELADA)),
        atendidas=Count("id", filter=Q(status=Consulta.Status.CONCLUIDA)),
    )
    return render(
        request,
        "recepcao/dashboard.html",
        {"appointments": appointments, "counts": counts, "today": today},
    )


@roles_required(User.Role.RECEPCAO, User.Role.ADMIN)
def daily_schedule(request):
    try:
        selected_date = date.fromisoformat(request.GET.get("data", ""))
    except ValueError:
        selected_date = timezone.localdate()
    appointments = list(appointments_for_date(date=selected_date))
    doctors = (
        Medico.objects.filter(ativo=True)
        .select_related("especialidade")
        .order_by("nome")
    )
    columns = [
        {
            "doctor": doctor,
            "appointments": [
                item for item in appointments if item.medico_id == doctor.id
            ],
        }
        for doctor in doctors
    ]
    return render(
        request,
        "recepcao/agenda.html",
        {
            "appointments": appointments,
            "doctor_columns": columns,
            "selected_date": selected_date,
        },
    )


@require_POST
@roles_required(User.Role.RECEPCAO, User.Role.ADMIN)
def update_appointment_status(request, pk, status):
    appointment = get_object_or_404(Consulta, pk=pk)
    allowed = {
        Consulta.Status.CONFIRMADA,
        Consulta.Status.PACIENTE_CHEGOU,
        Consulta.Status.AGUARDANDO,
        Consulta.Status.NAO_COMPARECEU,
    }
    try:
        if status not in allowed:
            raise ValidationError("A recepção não pode aplicar esse status.")
        transition_status(
            appointment=appointment, new_status=status, actor=request.user
        )
        messages.success(request, "Status atualizado com sucesso.")
    except ValidationError as error:
        messages.error(request, error.message)
    return redirect(request.POST.get("next") or "recepcao:daily-schedule")
