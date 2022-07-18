from rest_framework import permissions
from bus_operator import models as models_operator


class BusOperatorOnly(permissions.BasePermission):

    # edit_methods = "PATCH"

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role != "BUS_OPERATOR":
            return False

        profile = models_operator.BusOperatorProfile.objects.filter(user=request.user)
        if not profile.exists():
            return False

        return True


class AdminOnly(permissions.BasePermission):

    # edit_methods = ("PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "ADMIN":
            return True

        return False


class AdminGetOnlyOperatorPostPatchOnly(permissions.BasePermission):
    SAFE_METHODS = ["HEAD", "OPTIONS"]  # GET is not safe method here

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in self.SAFE_METHODS:
            return True

        if request.method == "GET" and request.user.role == "ADMIN":
            return True

        if request.method in ["POST", "PATCH"] and request.user.role == "BUS_OPERATOR":
            return True

        return False
