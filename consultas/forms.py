from django import forms

from accounts.models import User
from pacientes.models import Paciente
from medicos.models import Medico

from .services import save_appointment


class ConsultaForm(forms.Form):
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.none())
    medico = forms.ModelChoiceField(queryset=Medico.objects.none())
    data = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    hora_inicio = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    observacoes_administrativas = forms.CharField(required=False, widget=forms.Textarea)

    def __init__(self, *args, user, instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user, self.instance = user, instance
        self.fields["medico"].queryset = Medico.objects.filter(ativo=True).select_related("especialidade")
        if user.role == User.Role.PACIENTE:
            profile = getattr(user, "paciente", None)
            self.fields["paciente"].queryset = Paciente.objects.filter(pk=getattr(profile, "pk", None))
            self.fields["paciente"].initial = profile
            self.fields["paciente"].widget = forms.HiddenInput()
        else:
            self.fields["paciente"].queryset = Paciente.objects.select_related("user")

    def save(self):
        return save_appointment(paciente=self.cleaned_data["paciente"], medico=self.cleaned_data["medico"], data=self.cleaned_data["data"], hora_inicio=self.cleaned_data["hora_inicio"], actor=self.user, observacoes=self.cleaned_data["observacoes_administrativas"], instance=self.instance)
