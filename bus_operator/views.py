from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from . import serializers, models
from common.serializers import MediaSerializer


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


class BusOperatorProfileMediaView(APIView):
    """
    This Endpoint is used to set/update media in BusOperatorProfile
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, uuid, *args, **kwargs):
        objs = models.BusOperatorProfile.objects.get(id=uuid)
        serializer = serializers.BusOperatorProfileMediaSerializer(objs, many=False)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, uuid, *args, **kwargs):
        objs = models.BusOperatorProfile.objects.get(id=uuid)
        serializer = serializers.BusOperatorProfileMediaSerializer(
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

    def delete(self, request, uuid, *args, **kwargs):
        operator = models.BusOperatorProfile.objects.get(id=uuid)
        if operator.business_logo:
            operator.business_logo.delete()
        else:
            return Response(
                {
                    "success": False,
                    "errors": {
                        "business_logo": "Can't delete field that is already null"
                    },
                },
                status=status.HTTP_200_OK,
            )
        serializer = serializers.BusOperatorProfileMediaSerializer(
            operator, partial=False
        )
        return Response(
            {"success": True, "data": serializer.data},
            status=status.HTTP_200_OK,
        )
