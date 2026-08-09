from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "user",
        "acao",
        "content_type",
        "object_id",
        "ip_address",
    )
    list_filter = ("acao", "created_at")
    readonly_fields = tuple(field.name for field in AuditLog._meta.fields)
