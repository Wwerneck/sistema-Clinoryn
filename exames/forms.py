from django import forms
from .models import Exame


class ExameForm(forms.ModelForm):
    class Meta:
        model = Exame
        fields = ("tipo_exame", "descricao", "data_exame", "arquivo", "observacoes")
        widgets = {"data_exame": forms.DateInput(attrs={"type": "date"})}
