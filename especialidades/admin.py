from django.contrib import admin

from .models import Especialidade


@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo", "updated_at")
    list_filter = ("ativo",)
    search_fields = ("nome",)
