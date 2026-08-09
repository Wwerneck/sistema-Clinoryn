from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from accounts.models import User
from accounts.permissions import RolesRequiredMixin

from .forms import ConsultaForm
from .models import Consulta
from .services import cancel_appointment


class ConsultaListView(RolesRequiredMixin, ListView):
    allowed_roles = tuple(User.Role.values)
    model = Consulta
    paginate_by = 30
    template_name = "consultas/list.html"

    def get_queryset(self):
        qs = (
            super().get_queryset().select_related("paciente", "medico", "especialidade")
        )
        if self.request.user.role == User.Role.PACIENTE:
            qs = qs.filter(paciente=getattr(self.request.user, "paciente", None))
        elif self.request.user.role == User.Role.MEDICO:
            qs = qs.filter(medico=getattr(self.request.user, "medico", None))
        return qs


class ConsultaCreateView(RolesRequiredMixin, FormView):
    allowed_roles = (User.Role.ADMIN, User.Role.RECEPCAO, User.Role.PACIENTE)
    form_class = ConsultaForm
    template_name = "shared/form.html"
    success_url = reverse_lazy("consultas:list")
    extra_context = {"title": "Nova consulta"}

    def get_template_names(self):
        if self.request.headers.get("HX-Request") == "true":
            return ["consultas/_appointment_form.html"]
        return [self.template_name]

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "user": self.request.user}

    def form_valid(self, form):
        try:
            form.save()
        except ValidationError as error:
            form.add_error(None, error)
            return self.form_invalid(form)
        messages.success(self.request, "Consulta agendada com sucesso.")
        return super().form_valid(form)


class ConsultaUpdateView(ConsultaCreateView):
    extra_context = {"title": "Reagendar consulta"}

    def dispatch(self, request, *args, **kwargs):
        queryset = Consulta.objects.all()
        if request.user.is_authenticated and request.user.role == User.Role.PACIENTE:
            queryset = queryset.filter(paciente=getattr(request.user, "paciente", None))
        self.appointment = get_object_or_404(queryset, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.appointment
        if not self.request.POST:
            kwargs["initial"] = {
                "paciente": self.appointment.paciente,
                "medico": self.appointment.medico,
                "data": self.appointment.data,
                "hora_inicio": self.appointment.hora_inicio,
                "observacoes_administrativas": self.appointment.observacoes_administrativas,
            }
        return kwargs


def cancel(request, pk):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    qs = Consulta.objects.all()
    if request.user.role == User.Role.PACIENTE:
        qs = qs.filter(paciente=getattr(request.user, "paciente", None))
    elif request.user.role not in (User.Role.ADMIN, User.Role.RECEPCAO):
        qs = qs.none()
    appointment = get_object_or_404(qs, pk=pk)
    if request.method == "POST":
        try:
            cancel_appointment(appointment=appointment, actor=request.user)
            messages.success(request, "Consulta cancelada.")
        except ValidationError as error:
            messages.error(request, error.message)
    return redirect("consultas:list")
