from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from bus_operator import serializers_profile, serializers_bus
from bus_operator import models as models_operator

# Create your views here.


class ProfileView(APIView):
    """
    this View is responsible to operate on user profile for currently loggedin user
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.role == "BUS_OPERATOR":
            serializer = serializers_profile.BusOperatorProfileSerializer(
                request.user.opertor_profile
            )
            return Response(
                {"success": False, "data": serializer.data}, status=status.HTTP_200_OK
            )

        elif request.user.role == "CUSTOMER":
            return Response(
                {"success": False, "data": "not implemented"}, status=status.HTTP_200_OK
            )

        elif request.user.role == "ADMIN":
            return Response(
                {"success": False, "data": "not implemented"}, status=status.HTTP_200_OK
            )

        else:
            return Response(
                {"success": False, "data": "your profile data is inconsistent"},
                status=status.HTTP_200_OK,
            )

    def post(self, request, *args, **kwargs):
        return Response(
            {"success": False, "data": "not implemented"}, status=status.HTTP_200_OK
        )


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
