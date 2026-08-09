from django.contrib import admin

from .models import Recepcionista


@admin.register(Recepcionista)
class RecepcionistaAdmin(admin.ModelAdmin):
    list_display = ("nome", "cargo", "telefone", "ativo")
    list_filter = ("cargo", "ativo")
    search_fields = ("nome", "telefone")
    list_select_related = ("user",)
