from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, TemplateView

from accounts.models import User
from accounts.permissions import RolesRequiredMixin
from medicos.models import Medico

from .forms import BloqueioAgendaForm, DisponibilidadeForm
from .models import BloqueioAgenda, DisponibilidadeMedico


class AgendaListView(RolesRequiredMixin, TemplateView):
    allowed_roles = (User.Role.ADMIN, User.Role.MEDICO, User.Role.RECEPCAO)
    template_name = "agenda/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        disponibilidades = DisponibilidadeMedico.objects.select_related("medico", "medico__especialidade")
        bloqueios = BloqueioAgenda.objects.select_related("medico", "medico__especialidade")
        if self.request.user.role == User.Role.MEDICO:
            medico_id = getattr(getattr(self.request.user, "medico", None), "pk", None)
            disponibilidades = disponibilidades.filter(medico_id=medico_id)
            bloqueios = bloqueios.filter(medico_id=medico_id)
        elif medico_id := self.request.GET.get("medico"):
            disponibilidades = disponibilidades.filter(medico_id=medico_id)
            bloqueios = bloqueios.filter(medico_id=medico_id)
        context.update({
            "disponibilidades": disponibilidades,
            "bloqueios": bloqueios[:50],
            "medicos": Medico.objects.filter(ativo=True).order_by("nome"),
        })
        return context


class UserFormKwargsMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Agenda atualizada com sucesso.")
        return super().form_valid(form)


class DisponibilidadeCreateView(UserFormKwargsMixin, RolesRequiredMixin, CreateView):
    allowed_roles = (User.Role.ADMIN, User.Role.MEDICO)
    form_class = DisponibilidadeForm
    template_name = "shared/form.html"
    success_url = reverse_lazy("agenda:list")
    extra_context = {"title": "Nova disponibilidade"}


class BloqueioCreateView(UserFormKwargsMixin, RolesRequiredMixin, CreateView):
    allowed_roles = (User.Role.ADMIN, User.Role.MEDICO)
    form_class = BloqueioAgendaForm
    template_name = "shared/form.html"
    success_url = reverse_lazy("agenda:list")
    extra_context = {"title": "Novo bloqueio de agenda"}


class OwnershipDeleteMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == User.Role.MEDICO:
            queryset = queryset.filter(medico=getattr(self.request.user, "medico", None))
        return queryset


class DisponibilidadeDeleteView(OwnershipDeleteMixin, RolesRequiredMixin, DeleteView):
    allowed_roles = (User.Role.ADMIN, User.Role.MEDICO)
    model = DisponibilidadeMedico
    template_name = "shared/confirm_delete.html"
    success_url = reverse_lazy("agenda:list")


class BloqueioDeleteView(OwnershipDeleteMixin, RolesRequiredMixin, DeleteView):
    allowed_roles = (User.Role.ADMIN, User.Role.MEDICO)
    model = BloqueioAgenda
    template_name = "shared/confirm_delete.html"
    success_url = reverse_lazy("agenda:list")
