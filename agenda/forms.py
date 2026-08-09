from django import forms
from django.core.exceptions import ValidationError

from accounts.models import User
from medicos.models import Medico

from .models import BloqueioAgenda, DisponibilidadeMedico


class UserScopedDoctorFormMixin:
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["medico"].queryset = Medico.objects.filter(ativo=True).select_related("especialidade")
        if user.role == User.Role.MEDICO:
            medico = getattr(user, "medico", None)
            self.fields["medico"].queryset = Medico.objects.filter(pk=getattr(medico, "pk", None))
            self.fields["medico"].initial = medico
            self.fields["medico"].widget = forms.HiddenInput()

    def clean_medico(self):
        medico = self.cleaned_data.get("medico")
        if self.user.role == User.Role.MEDICO:
            own_profile = getattr(self.user, "medico", None)
            if not own_profile or medico != own_profile:
                raise ValidationError("Seu usuário não possui um perfil médico válido.")
        return medico


class DisponibilidadeForm(UserScopedDoctorFormMixin, forms.ModelForm):
    class Meta:
        model = DisponibilidadeMedico
        fields = ("medico", "dia_semana", "hora_inicio", "hora_fim", "duracao_consulta", "ativo")
        widgets = {"hora_inicio": forms.TimeInput(attrs={"type": "time"}), "hora_fim": forms.TimeInput(attrs={"type": "time"})}


class BloqueioAgendaForm(UserScopedDoctorFormMixin, forms.ModelForm):
    class Meta:
        model = BloqueioAgenda
        fields = ("medico", "data", "hora_inicio", "hora_fim", "motivo", "observacao")
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
            "hora_inicio": forms.TimeInput(attrs={"type": "time"}),
            "hora_fim": forms.TimeInput(attrs={"type": "time"}),
        }
