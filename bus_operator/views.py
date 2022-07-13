from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from . import serializers, models


class BusOperatorProfileListView(APIView):
    """
    List View for BusOperatorProfile objects
    it is responsible to perform operation on collection of object
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        objs = models.BusOperatorProfile.objects.all()
        serializer = serializers.BusOperatorProfileSerializer(objs, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        serializer = serializers.BusOperatorProfileSerializer(
            data=request.data, partial=True
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


class BusOperatorProfileDetailView(APIView):
    """
    Details View for BusOperatorProfile objects
    it is responsible to perform operation on single object
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, uuid, *args, **kwargs):
        objs = models.BusOperatorProfile.objects.get(id=uuid)
        serializer = serializers.BusOperatorProfileSerializer(objs, many=False)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, uuid, *args, **kwargs):
        objs = models.BusOperatorProfile.objects.get(id=uuid)
        serializer = serializers.BusOperatorProfileSerializer(
            objs, data=request.data, partial=False
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
