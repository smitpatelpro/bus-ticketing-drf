from multiprocessing import context
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import permissions
from . import models, serializers_profile
from authentication.permission_classes import *


class BusOperatorProfileView(APIView):
    """
    Its responsible to provide operations to Bus Operator and Admin for both single and multiple objects
    """

    permission_classes = [
        (AdminOnly & (GetOnly | PatchOnly)) | (BusOperatorProfileRequired & PostOnly)
    ]

    def get(self, request, uuid=None, *args, **kwargs):
        if uuid:
            try:
                objs = models.BusOperatorProfile.objects.get(id=uuid)
            except models.BusOperatorProfile.DoesNotExist:
                return Response(
                    {"success": False, "message": "Resource does not exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            many = False
        else:
            objs = models.BusOperatorProfile.objects.all()
            many = True

        serializer = serializers_profile.BusOperatorProfileSerializer(objs, many=many)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request, uuid=None, *args, **kwargs):
        serializer = serializers_profile.BusOperatorProfileSerializer(
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

    # TODO: Resolve permission issue for request with uuid
    def patch(self, request, uuid=None, *args, **kwargs):
        if not uuid == None:
            objs = models.BusOperatorProfile.objects.get(id=uuid)
            serializer = serializers_profile.BusOperatorProfileSerializer(
                objs, data=request.data, partial=True, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"success": True, "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"success": False, "message": "PATCH is not permitted on collection"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Bus Operator Profile Views
class ProfileDetailView(APIView):
    """
    Details View for currently loggedin operator to access his BusOperatorProfile objects
    """

    permission_classes = [BusOperatorProfileRequired & (GetOnly | PatchOnly)]

    def get(self, request, *args, **kwargs):
        serializer = serializers_profile.BusOperatorProfileSerializer(
            request.user.busoperatorprofile_user
        )
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        if "ratings" in request.data:
            del request.data["ratings"]
        serializer = serializers_profile.BusOperatorProfileSerializer(
            request.user.busoperatorprofile_user,
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
    Media access for currently loggedin BusOperatorProfile
    """

    permission_classes = [
        BusOperatorProfileRequired & (GetOnly | PatchOnly | DeleteOnly)
    ]

    def get(self, request, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        serializer = serializers_profile.BusOperatorProfileMediaSerializer(profile)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
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
