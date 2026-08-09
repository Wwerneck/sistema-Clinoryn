from django.contrib import admin
from .models import Consulta


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ("data", "hora_inicio", "paciente", "medico", "status", "valor")
    list_filter = ("status", "data", "especialidade")
    search_fields = ("paciente__nome_completo", "medico__nome")
