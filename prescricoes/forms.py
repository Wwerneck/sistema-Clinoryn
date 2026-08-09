from django import forms
from django.forms import inlineformset_factory
from .models import ItemPrescricao, Prescricao


class PrescricaoForm(forms.ModelForm):
    class Meta:
        model = Prescricao
        fields = ("observacoes",)


ItemFormSet = inlineformset_factory(
    Prescricao,
    ItemPrescricao,
    fields=("medicamento", "dosagem", "frequencia", "duracao", "orientacoes"),
    extra=2,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
