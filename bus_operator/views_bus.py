from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from . import models, decorators, serializers_bus
from common.serializers import MediaSerializer
from django.utils.decorators import method_decorator

class BusListView(APIView):
    """
    List All Bus related to BusOperatorProfile
    """

    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(decorators.bus_operator_profile_required)
    def get(self, request, profile, *args, **kwargs):
        buses = models.Bus.objects.filter(operator=profile)
        serializer = serializers_bus.BusSerializer(buses, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    @method_decorator(decorators.bus_operator_profile_required)
    def post(self, request, profile, *args, **kwargs):
        serializer = serializers_bus.BusSerializer(
            data=request.data, partial=True, context={'profile': profile}
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


class BusDetailView(APIView):
    """
    Get Details of specific bus
    """

    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(decorators.bus_operator_profile_required)
    def get(self, request, profile, uuid, *args, **kwargs):
        bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
        if not bus:
            return Response(
                {"success": False}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = serializers_bus.BusSerializer(
            bus, many=False
        )
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    @method_decorator(decorators.bus_operator_profile_required)
    def patch(self, request, profile, uuid, *args, **kwargs):
        bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
        serializer = serializers_bus.BusSerializer(
            bus, data=request.data, partial=False
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

# class BusPhotosView(APIView):
#     """
#     Get Details of specific bus
#     """

#     permission_classes = [permissions.IsAuthenticated]

#     @method_decorator(decorators.bus_operator_profile_required)
#     def patch(self, request, profile, uuid, *args, **kwargs):
#         bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
#         serializer = serializers_bus.BusSerializer(
#             bus, data=request.data, partial=False
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