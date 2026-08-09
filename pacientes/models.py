from django.conf import settings
from django.db import models

from accounts.validators import only_digits, validate_cpf, validate_uf


class Paciente(models.Model):
    class Sexo(models.TextChoices):
        FEMININO = "F", "Feminino"
        MASCULINO = "M", "Masculino"
        OUTRO = "O", "Outro"
        NAO_INFORMADO = "N", "Prefiro não informar"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="paciente")
    nome_completo = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True, validators=[validate_cpf])
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    endereco = models.CharField(max_length=180)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, validators=[validate_uf])
    cep = models.CharField(max_length=8)
    contato_emergencia = models.CharField(max_length=150, blank=True)
    telefone_emergencia = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("nome_completo",)
        indexes = [models.Index(fields=("nome_completo",)), models.Index(fields=("telefone",))]

    def save(self, *args, **kwargs):
        self.cpf = only_digits(self.cpf)
        self.cep = only_digits(self.cep)
        self.estado = self.estado.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_completo
