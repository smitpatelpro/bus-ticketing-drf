from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from bus_operator import serializers_profile, serializers_bus
from bus_operator import models as models_operator


class AmenitiesListView(APIView):
    """
    List View for ALL Bus Amenities
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        amenities = models_operator.BusAmenity.objects.all()
        serializer = serializers_bus.BusAmenitySerializer(amenities, many=True)
        return Response(
            {"success": True, "data": serializer.data},
            status=status.HTTP_200_OK,
        )
