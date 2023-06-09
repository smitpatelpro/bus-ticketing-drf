from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.permission_classes import *
from bus_operator import serializers_bus, models as models_operator
from . import models, serializers


class CustomerProfileView(APIView):
    """
    It provides access to any customer profile
    """

    permission_classes = [
        (AdminOnly & (GetOnly | PatchOnly)) | (CustomerOnly & PostOnly)
    ]

    def get(self, request, uuid=None, *args, **kwargs):
        if uuid:
            try:
                objs = models.CustomerProfile.objects.get(id=uuid)
            except models.CustomerProfile.DoesNotExist:
                return Response(
                    {"success": False, "message": "Resource does not exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = serializers.CustomerProfileSerializer(objs, many=False)
        else:
            objs = models.CustomerProfile.objects.all()
            serializer = serializers.CustomerProfileSerializer(objs, many=True)

        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request, uuid=None, *args, **kwargs):
        serializer = serializers.CustomerProfileSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, uuid=None, *args, **kwargs):
        objs = models.CustomerProfile.objects.get(id=uuid)
        serializer = serializers.CustomerProfileSerializer(
            objs, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Customer Profile Views
class ProfileDetailView(APIView):
    """
    it provides profile operation for currently loggedin customer profile only
    """

    permission_classes = [CustomerOnly]

    def get(self, request, *args, **kwargs):
        serializer = serializers.CustomerProfileSerializer(
            request.user.customerprofile_user
        )
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        serializer = serializers.CustomerProfileSerializer(
            request.user.customerprofile_user,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Views for Current User
class ProfileMediaView(APIView):
    """
    Media access for Current CustomerProfile
    """

    permission_classes = [CustomerOnly]

    def get(self, request, *args, **kwargs):
        profile = request.user.customerprofile_user
        serializer = serializers.CustomerProfileMediaSerializer(profile)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        profile = request.user.customerprofile_user
        serializer = serializers.CustomerProfileMediaSerializer(
            profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Customer Ticket Views
class TicketView(APIView):

    permission_classes = [CustomerOnly]

    def get(self, request, uuid=None, *args, **kwargs):
        if uuid:
            profile = request.user.customerprofile_user
            tickets = models_operator.Ticket.objects.filter(
                customer=profile, id=uuid
            ).first()
            many = False
            pass
        else:
            profile = request.user.customerprofile_user
            tickets = models_operator.Ticket.objects.filter(customer=profile)
            many = True

        serializer = serializers_bus.TicketSerializer(tickets, many=many)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request, uuid=None, *args, **kwargs):
        request.data["customer"] = str(request.user.customerprofile_user.id)
        serializer = serializers_bus.TicketSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, uuid=None, *args, **kwargs):
        now = timezone.now()
        profile = request.user.customerprofile_user
        if uuid:
            ticket = models_operator.Ticket.objects.filter(
                customer=profile, id=uuid
            ).first()
            if not ticket:
                return Response(
                    {"success": False, "message": "ticket does not exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if ticket.journey_date >= now.date():
                return Response(
                    {
                        "success": False,
                        "message": "review can be only post after journey_date",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            rating = request.data.get("rating")
            print("rating: ", rating)
            if rating and 0 <= rating and rating <= 10:
                ticket.rating = rating
                ticket.save(update_fields=["rating"])
            else:
                return Response(
                    {
                        "success": False,
                        "message": "invalid rating value. please include rating parameter with integer value in range 0 to 10",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(
                {"success": True},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"success": False, "message": "PATCH is not permitted on collection"},
                status=status.HTTP_400_BAD_REQUEST,
            )
