from django import forms
from django.contrib.auth.password_validation import validate_password

from accounts.models import User
from accounts.services import create_user_with_profile
from accounts.validators import only_digits, validate_cpf

from .models import Paciente


class PacienteCreateForm(forms.ModelForm):
    username = forms.CharField(label="Usuário", max_length=150)
    password = forms.CharField(label="Senha inicial", widget=forms.PasswordInput, validators=[validate_password])
    cpf = forms.CharField(label="CPF", max_length=14)

    class Meta:
        model = Paciente
        exclude = ("user", "created_at", "updated_at")
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Este usuário já está em uso.")
        return username

    def clean_cpf(self):
        cpf = only_digits(self.cleaned_data["cpf"])
        validate_cpf(cpf)
        return cpf

    def save(self, commit=True):
        data = self.cleaned_data.copy()
        return create_user_with_profile(role=User.Role.PACIENTE, profile_model=Paciente, profile_data=data).paciente
