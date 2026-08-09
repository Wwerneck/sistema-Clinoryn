from .context import current_request
from .models import AuditLog


def log_action(*, action, user=None, obj=None, metadata=None):
    request = current_request.get()
    if user is None and request is not None and request.user.is_authenticated:
        user = request.user
    forwarded = (
        request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
        if request
        else ""
    )
    ip = forwarded or (request.META.get("REMOTE_ADDR") if request else None)
    return AuditLog.objects.create(
        user=user,
        acao=action,
        content_type=obj._meta.label_lower if obj else "",
        object_id=str(obj.pk) if obj and obj.pk else "",
        ip_address=ip or None,
        user_agent=(request.META.get("HTTP_USER_AGENT", "")[:255] if request else ""),
        metadata=metadata or {},
    )
