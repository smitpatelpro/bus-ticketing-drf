from rest_framework import permissions
# from bus_operator import models as models_operator
# from customer import models as models_customer

SAFE_METHODS = ["HEAD", "OPTIONS"]

# ==============================
# New Atomic Permission Classes
# ==============================
# NOTE: here, we have defined smaller set of responsible classes 
# and are combined using logical operations
class BusOperatorProfileRequired(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != "BUS_OPERATOR":
            return False
        if (
            hasattr(request.user, "busoperatorprofile_user")
            and (request.user.busoperatorprofile_user is not None)
            and request.user.busoperatorprofile_user.deleted_at is None
        ):
            return True

        return False


class ApprovedBusOperatorProfileRequired(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != "BUS_OPERATOR":
            return False

        if (
            hasattr(request.user, "busoperatorprofile_user")
            and (request.user.busoperatorprofile_user is not None)
            and request.user.busoperatorprofile_user.deleted_at is None
            and request.user.busoperatorprofile_user.approval_status == "APPROVED"
        ):
            return True

        return False


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != "ADMIN":
            return False
        return True


class BusOperatorOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != "BUS_OPERATOR":
            return False

        if (
            hasattr(request.user, "busoperatorprofile_user")
            and (request.user.busoperatorprofile_user is not None)
            and request.user.busoperatorprofile_user.deleted_at is None
        ):
            return True
        return False


class CustomerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != "CUSTOMER":
            return False

        if (
            hasattr(request.user, "customerprofile_user")
            and (request.user.customerprofile_user is not None)
            and request.user.customerprofile_user.deleted_at is None
        ):
            return True

        return True


class GetOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == "GET":
            return True


class PostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == "POST":
            return True


class PatchOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == "PATCH":
            return True


class DeleteOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == "DELETE":
            return True

# ===============================================
# Old Code for reference to understand bad design
# ===============================================
'''

# TODO: Normalize permissions and break into separate class
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

'''