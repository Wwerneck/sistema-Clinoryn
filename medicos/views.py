from datetime import date

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, ListView

from accounts.models import User
from accounts.permissions import RolesRequiredMixin, roles_required
from consultas.models import Consulta
from consultas.services import transition_status

from .forms import MedicoCreateForm
from .models import Medico
from .selectors import doctor_appointments, doctor_dashboard_data


class MedicoListView(RolesRequiredMixin, ListView):
    allowed_roles = (User.Role.ADMIN, User.Role.RECEPCAO, User.Role.PACIENTE)
    model = Medico
    paginate_by = 20
    template_name = "medicos/list.html"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("especialidade", "user")
        if self.request.user.role != User.Role.ADMIN:
            queryset = queryset.filter(ativo=True)
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(Q(nome__icontains=query) | Q(crm__icontains=query) | Q(especialidade__nome__icontains=query))
        return queryset


class MedicoCreateView(RolesRequiredMixin, CreateView):
    allowed_roles = (User.Role.ADMIN,)
    form_class = MedicoCreateForm
    template_name = "shared/form.html"
    success_url = reverse_lazy("medicos:list")
    extra_context = {"title": "Novo médico"}


class MedicoDeleteView(RolesRequiredMixin, DeleteView):
    allowed_roles = (User.Role.ADMIN,)
    model = Medico
    template_name = "medicos/confirm_delete.html"
    success_url = reverse_lazy("medicos:list")

    def form_valid(self, form):
        with transaction.atomic():
            self.object.ativo = False
            self.object.save(update_fields=("ativo", "updated_at"))
            self.object.user.is_active = False
            self.object.user.save(update_fields=("is_active",))
        messages.success(
            self.request,
            "Médico desativado com sucesso. Todo o histórico foi preservado.",
        )
        return redirect(self.success_url)


def _own_doctor(user):
    return get_object_or_404(Medico, user=user, ativo=True)


@roles_required(User.Role.MEDICO)
def medical_dashboard(request):
    return render(request, "medicos/dashboard.html", doctor_dashboard_data(medico=_own_doctor(request.user)))


@roles_required(User.Role.MEDICO)
def own_schedule(request):
    try:
        selected_date = date.fromisoformat(request.GET.get("data", ""))
    except ValueError:
        selected_date = timezone.localdate()
    appointments = doctor_appointments(medico=_own_doctor(request.user)).filter(data=selected_date).order_by("hora_inicio")
    return render(request, "medicos/agenda.html", {"appointments": appointments, "selected_date": selected_date})


@require_POST
@roles_required(User.Role.MEDICO)
def update_attendance_status(request, pk, status):
    appointment = get_object_or_404(Consulta, pk=pk, medico=_own_doctor(request.user))
    if status not in (Consulta.Status.EM_ATENDIMENTO, Consulta.Status.CONCLUIDA):
        messages.error(request, "O médico não pode aplicar esse status.")
        return redirect("medicos:dashboard")
    try:
        transition_status(appointment=appointment, new_status=status, actor=request.user)
        messages.success(request, "Atendimento atualizado com sucesso.")
    except ValidationError as error:
        messages.error(request, error.message)
    return redirect(request.POST.get("next") or "medicos:dashboard")
