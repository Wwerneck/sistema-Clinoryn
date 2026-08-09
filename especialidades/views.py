from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from accounts.models import User
from accounts.permissions import RolesRequiredMixin

from .forms import EspecialidadeForm
from .models import Especialidade


class EspecialidadeListView(RolesRequiredMixin, ListView):
    allowed_roles = (User.Role.ADMIN, User.Role.MEDICO, User.Role.RECEPCAO, User.Role.PACIENTE)
    model = Especialidade
    paginate_by = 20
    template_name = "especialidades/list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role != User.Role.ADMIN:
            queryset = queryset.filter(ativo=True)
        return queryset


class EspecialidadeCreateView(RolesRequiredMixin, CreateView):
    allowed_roles = (User.Role.ADMIN,)
    form_class = EspecialidadeForm
    template_name = "shared/form.html"
    success_url = reverse_lazy("especialidades:list")
    extra_context = {"title": "Nova especialidade"}


class EspecialidadeUpdateView(RolesRequiredMixin, UpdateView):
    allowed_roles = (User.Role.ADMIN,)
    model = Especialidade
    form_class = EspecialidadeForm
    template_name = "shared/form.html"
    success_url = reverse_lazy("especialidades:list")
    extra_context = {"title": "Editar especialidade"}
