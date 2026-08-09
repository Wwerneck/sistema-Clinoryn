from django.contrib import admin

from .models import Medico


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "crm", "especialidade", "ativo", "valor_consulta")
    list_filter = ("ativo", "especialidade")
    search_fields = ("nome", "crm", "especialidade__nome")
    list_select_related = ("user", "especialidade")
