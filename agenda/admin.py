from django.contrib import admin

from .models import BloqueioAgenda, DisponibilidadeMedico


@admin.register(DisponibilidadeMedico)
class DisponibilidadeAdmin(admin.ModelAdmin):
    list_display = ("medico", "dia_semana", "hora_inicio", "hora_fim", "duracao_consulta", "ativo")
    list_filter = ("dia_semana", "ativo", "medico")
    list_select_related = ("medico",)


@admin.register(BloqueioAgenda)
class BloqueioAgendaAdmin(admin.ModelAdmin):
    list_display = ("medico", "data", "hora_inicio", "hora_fim", "motivo")
    list_filter = ("motivo", "data", "medico")
    list_select_related = ("medico",)
