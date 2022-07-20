from rest_framework import permissions
from bus_operator import models as models_operator
from customer import models as models_customer


class BusOperatorOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != "BUS_OPERATOR":
            return False

        if hasattr(request.user, "busoperatorprofile_user") and (request.user.busoperatorprofile_user is not None) and request.user.busoperatorprofile_user.deleted_at is None:
            return True
        
        # # TODO:[Done] Lazyload operator profile using request.user.busoperator_user:
        # profile = models_operator.BusOperatorProfile.objects.filter(user=request.user)
        # if not profile.exists():
        #     return False

        return False


class CustomerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != "CUSTOMER":
            return False

        if hasattr(request.user, "customerprofile_user") and (request.user.customerprofile_user is not None) and request.user.customerprofile_user.deleted_at is None:
            return True

        return True


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "ADMIN":
            return True

        return False


class AdminGetPatchOnlyOperatorPostOnly(permissions.BasePermission):
    SAFE_METHODS = ["HEAD", "OPTIONS"]  # GET is not safe method here

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in self.SAFE_METHODS:
            return True

        if request.method in ["GET", "PATCH"] and request.user.role == "ADMIN":
            return True

        if request.method == "POST" and request.user.role == "BUS_OPERATOR":
            return True

        return False


class AdminGetPatchOnlyCustomerPostOnly(permissions.BasePermission):
    SAFE_METHODS = ["HEAD", "OPTIONS"]  # GET is not safe method here

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in self.SAFE_METHODS:
            return True
        
        if request.method in ["GET", "PATCH"] and request.user.role == "ADMIN":
            return True

        if request.method == "POST" and request.user.role == "CUSTOMER":
            return True

        return False
