from multiprocessing import context
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from . import models, serializers
from common.serializers import MediaSerializer
from django.utils.decorators import method_decorator
from authentication.permission_classes import *
from bus_operator import serializers_bus, models as models_operator

class CustomerProfileView(APIView):
    """
    List View for ALL CustomerProfile objects
    it is responsible to perform operation on collection of object
    """

    permission_classes = [AdminGetPatchOnlyCustomerPostOnly]

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


# class CustomerProfileDetailView(APIView):
#     """
#     Details View for Specific CustomerProfile objects
#     Only for admin
#     """

#     permission_classes = [AdminOnly]

#     # TODO: merge detail view with list view above
#     def get(self, request, uuid=None, *args, **kwargs):
#         try:
#             objs = models.CustomerProfile.objects.get(id=uuid)
#         except models.CustomerProfile.DoesNotExist:
#             return Response(
#                 {"success": False, "message": "Resource does not exists"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         serializer = serializers.CustomerProfileSerializer(objs, many=False)
#         return Response(
#             {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
#         )

#     # TODO: put this patch to above view
#     def patch(self, request, uuid, *args, **kwargs):
#         objs = models.CustomerProfile.objects.get(id=uuid)
#         serializer = serializers.CustomerProfileSerializer(
#             objs, data=request.data, partial=True, context={"request": request}
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
#             )
#         return Response(
#             {"success": False, "errors": serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST,
#         )


# Customer Profile Views
class ProfileDetailView(APIView):
    """
    Details View for Specific CustomerProfile objects
    it is responsible to perform operation on single object
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
    """
    Details View for Specific CustomerProfile objects
    it is responsible to perform operation on single object
    """

    permission_classes = [CustomerOnly]

    def get(self, request, uuid=None, *args, **kwargs):
        if uuid:
            pass
        else:
            profile = request.user.customerprofile_user
            tickets = models_operator.Ticket.objects.filter(customer=profile)
            serializer = serializers_bus.TicketSerializer(tickets, many=True)
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )

    def post(self, request, uuid=None, *args, **kwargs):
        request.data["customer"] = str(request.user.customerprofile_user.id)
        # bus = models.Bus.objects.filter(id=uuid).first()
        # if not bus:
        #     return Response(
        #         {"success": False, "message": "bus does not exists"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        # distance = bus.get_distance()
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