from django.views.generic import ListView
from accounts.models import User
from accounts.permissions import RolesRequiredMixin
from .models import AuditLog


class AuditLogListView(RolesRequiredMixin, ListView):
    allowed_roles = (User.Role.ADMIN,)
    model = AuditLog
    paginate_by = 50
    template_name = "auditoria/list.html"

    def get_queryset(self):
        qs = super().get_queryset().select_related("user")
        if action := self.request.GET.get("acao"):
            qs = qs.filter(acao=action)
        return qs
