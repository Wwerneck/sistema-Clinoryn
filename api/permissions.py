from rest_framework.permissions import BasePermission

from accounts.models import User


class HasRole(BasePermission):
    allowed_roles = ()

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )


class IsAdminRole(HasRole):
    allowed_roles = (User.Role.ADMIN,)


class IsDoctorRole(HasRole):
    allowed_roles = (User.Role.MEDICO,)


class IsReceptionRole(HasRole):
    allowed_roles = (User.Role.RECEPCAO,)


class IsPatientRole(HasRole):
    allowed_roles = (User.Role.PACIENTE,)


class IsAdminOrReceptionRole(HasRole):
    allowed_roles = (User.Role.ADMIN, User.Role.RECEPCAO)


class IsClinicalStaffRole(HasRole):
    allowed_roles = (User.Role.ADMIN, User.Role.MEDICO)
