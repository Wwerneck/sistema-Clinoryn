from django import forms
from django.contrib.auth.password_validation import validate_password

from accounts.models import User
from accounts.services import create_user_with_profile

from .models import Recepcionista


class RecepcionistaCreateForm(forms.ModelForm):
    username = forms.CharField(label="Usuário", max_length=150)
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Senha inicial", widget=forms.PasswordInput, validators=[validate_password])

    class Meta:
        model = Recepcionista
        exclude = ("user", "created_at", "updated_at")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Este usuário já está em uso.")
        return username

    def save(self, commit=True):
        data = self.cleaned_data.copy()
        email = data.pop("email")
        user = create_user_with_profile(role=User.Role.RECEPCAO, profile_model=Recepcionista, profile_data=data)
        user.email = email
        user.save(update_fields=("email",))
        return user.recepcionista
