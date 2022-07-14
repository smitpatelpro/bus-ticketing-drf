from . import models
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status


def bus_operator_profile_required(function):
    def wrap(request, *args, **kwargs):
        profile = models.BusOperatorProfile.objects.filter(user=request.user).first()
        if profile:
            return function(request, profile, *args, **kwargs)
        else:
            return Response(
                {
                    "success": False,
                    "message": "Only bus operators are allowed to access",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
            # raise PermissionDenied("Only bus operators are allowed to access")
            pass

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
