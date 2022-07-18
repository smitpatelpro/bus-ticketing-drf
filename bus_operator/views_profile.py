from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from . import models, serializers_profile
from common.serializers import MediaSerializer
from django.utils.decorators import method_decorator

# Views for all objects
class BusOperatorProfileListView(APIView):
    """
    List View for ALL BusOperatorProfile objects
    it is responsible to perform operation on collection of object
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        objs = models.BusOperatorProfile.objects.all()
        serializer = serializers_profile.BusOperatorProfileSerializer(objs, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        serializer = serializers_profile.BusOperatorProfileSerializer(
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
    Details View for Specific BusOperatorProfile objects
    it is responsible to perform operation on single object
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, uuid, *args, **kwargs):
        try:
            objs = models.BusOperatorProfile.objects.get(id=uuid)
        except models.BusOperatorProfile.DoesNotExist:
            return Response(
                {"success": False, "message": "Resource does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = serializers_profile.BusOperatorProfileSerializer(objs, many=False)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, uuid, *args, **kwargs):
        objs = models.BusOperatorProfile.objects.get(id=uuid)
        serializer = serializers_profile.BusOperatorProfileSerializer(
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
    Media access for Specific BusOperatorProfile
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, uuid, *args, **kwargs):
        profile = models.BusOperatorProfile.objects.get(id=uuid)
        serializer = serializers_profile.BusOperatorProfileMediaSerializer(
            profile, many=False
        )
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, uuid, *args, **kwargs):
        profile = models.BusOperatorProfile.objects.get(id=uuid)
        serializer = serializers_profile.BusOperatorProfileMediaSerializer(
            profile, data=request.data, partial=False
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
        return Response(
            {"success": True},
            status=status.HTTP_200_OK,
        )


# Views for Current User
class ProfileMediaView(APIView):
    """
    Media access for Current BusOperatorProfile
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        serializer = serializers_profile.BusOperatorProfileMediaSerializer(profile)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        serializer = serializers_profile.BusOperatorProfileMediaSerializer(
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

    def delete(self, request, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        if profile.business_logo:
            profile.business_logo.delete()
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
        return Response(
            {"success": True},
            status=status.HTTP_200_OK,
        )
