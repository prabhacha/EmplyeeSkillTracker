from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.role == "Admin"
        )


class IsManager(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.role == "Manager"
        )


class IsEmployee(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.role == "Employee"
        )


class IsAdminOrManager(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.role in [
                "Admin",
                "Manager"
            ]
        )