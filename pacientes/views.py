from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.utils import timezone

from accounts.models import User
from accounts.permissions import RolesRequiredMixin

from .forms import PacienteCreateForm
from .models import Paciente


class PacienteListView(RolesRequiredMixin, ListView):
    allowed_roles = (User.Role.ADMIN, User.Role.MEDICO, User.Role.RECEPCAO)
    model = Paciente
    paginate_by = 20
    template_name = "pacientes/list.html"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("user")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(nome_completo__icontains=query)
                | Q(cpf__icontains=query)
                | Q(telefone__icontains=query)
                | Q(email__icontains=query)
            )
        return queryset


class PacienteCreateView(RolesRequiredMixin, CreateView):
    allowed_roles = (User.Role.ADMIN, User.Role.RECEPCAO)
    form_class = PacienteCreateForm
    template_name = "shared/form.html"
    success_url = reverse_lazy("pacientes:list")
    extra_context = {"title": "Novo paciente"}


def patient_detail(request, pk):
    if not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login

        return redirect_to_login(request.get_full_path())
    allowed = request.user.role in (User.Role.ADMIN, User.Role.RECEPCAO)
    patient = get_object_or_404(Paciente.objects.select_related("user"), pk=pk)
    if request.user.role == User.Role.PACIENTE:
        allowed = patient.user_id == request.user.id
    elif request.user.role == User.Role.MEDICO:
        allowed = patient.consultas.filter(
            medico=getattr(request.user, "medico", None)
        ).exists()
    if not allowed:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied
    consultations = patient.consultas.select_related(
        "medico", "especialidade"
    ).order_by("-data", "-hora_inicio")
    return render(
        request,
        "pacientes/detail.html",
        {
            "patient": patient,
            "consultations": consultations[:8],
            "total_consultations": consultations.count(),
            "last_consultation": consultations.first(),
            "next_consultation": consultations.order_by("data", "hora_inicio")
            .filter(data__gte=timezone.localdate())
            .first(),
            "total_paid": patient.pagamentos.filter(status="PAGO").aggregate(
                total=Sum("valor")
            )["total"]
            or 0,
            "show_clinical": request.user.role == User.Role.MEDICO,
        },
    )
