from django import forms

from .models import EvolucaoClinica, Prontuario


class ProntuarioForm(forms.ModelForm):
    class Meta:
        model = Prontuario
        fields = ("queixa_principal", "sintomas", "historico", "alergias", "antecedentes", "doencas_preexistentes", "medicamentos_em_uso", "historico_familiar", "diagnostico", "observacoes")


class EvolucaoClinicaForm(forms.ModelForm):
    class Meta:
        model = EvolucaoClinica
        fields = ("descricao",)
