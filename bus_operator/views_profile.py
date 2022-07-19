from multiprocessing import context
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from . import models, serializers_profile
from common.serializers import MediaSerializer
from django.utils.decorators import method_decorator
from authentication.permission_classes import *


class BusOperatorProfileListView(APIView):
    """
    List View for ALL BusOperatorProfile objects
    it is responsible to perform operation on collection of object
    """

    permission_classes = [AdminGetOnlyOperatorPostPatchOnly]

    def get(self, request, *args, **kwargs):
        objs = models.BusOperatorProfile.objects.all()
        serializer = serializers_profile.BusOperatorProfileSerializer(objs, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
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


class BusOperatorProfileDetailView(APIView):
    """
    Details View for Specific BusOperatorProfile objects
    Only for admin
    """

    permission_classes = [AdminOnly]

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


# Bus Operator Profile Views
class ProfileDetailView(APIView):
    """
    Details View for Specific BusOperatorProfile objects
    it is responsible to perform operation on single object
    """

    permission_classes = [BusOperatorOnly]

    def get(self, request, *args, **kwargs):
        serializer = serializers_profile.BusOperatorProfileSerializer(
            request.user.busoperatorprofile_user
        )
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
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


"""
This Feature is for admins, but its not required as we cant allow admins to perform this also
"""
# class BusOperatorProfileMediaView(APIView):
#     """
#     Media access for Specific BusOperatorProfile
#     """

#     permission_classes = [BusOperatorOnly]

#     def get(self, request, uuid, *args, **kwargs):
#         profile = models.BusOperatorProfile.objects.get(id=uuid)
#         serializer = serializers.BusOperatorProfileMediaSerializer(profile, many=False)
#         return Response(
#             {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
#         )

#     def patch(self, request, uuid, *args, **kwargs):
#         profile = models.BusOperatorProfile.objects.get(id=uuid)
#         serializer = serializers.BusOperatorProfileMediaSerializer(
#             profile, data=request.data, partial=False
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

#     def delete(self, request, uuid, *args, **kwargs):
#         operator = models.BusOperatorProfile.objects.get(id=uuid)
#         if operator.business_logo:
#             operator.business_logo.delete()
#         else:
#             return Response(
#                 {
#                     "success": False,
#                     "errors": {
#                         "business_logo": "Can't delete field that is already null"
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         return Response(
#             {"success": True},
#             status=status.HTTP_200_OK,
#         )


# Views for Current User
class ProfileMediaView(APIView):
    """
    Media access for Current BusOperatorProfile
    """

    permission_classes = [BusOperatorOnly]

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
