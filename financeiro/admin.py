from django.contrib import admin
from .models import Pagamento


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = (
        "consulta",
        "valor",
        "forma_pagamento",
        "status",
        "data_pagamento",
        "registrado_por",
    )
    list_filter = ("status", "forma_pagamento")
