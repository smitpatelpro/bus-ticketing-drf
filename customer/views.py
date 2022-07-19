from multiprocessing import context
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from . import models, serializers
from common.serializers import MediaSerializer
from django.utils.decorators import method_decorator
from authentication.permission_classes import *


class CustomerProfileListView(APIView):
    """
    List View for ALL CustomerProfile objects
    it is responsible to perform operation on collection of object
    """

    permission_classes = [AdminGetOnlyCustomerPostPatchOnly]

    def get(self, request, *args, **kwargs):
        objs = models.CustomerProfile.objects.all()
        serializer = serializers.CustomerProfileSerializer(objs, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
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


class CustomerProfileDetailView(APIView):
    """
    Details View for Specific CustomerProfile objects
    Only for admin
    """

    permission_classes = [AdminOnly]

    def get(self, request, uuid, *args, **kwargs):
        try:
            objs = models.CustomerProfile.objects.get(id=uuid)
        except models.CustomerProfile.DoesNotExist:
            return Response(
                {"success": False, "message": "Resource does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = serializers.CustomerProfileSerializer(objs, many=False)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, uuid, *args, **kwargs):
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

    # def delete(self, request, *args, **kwargs):
    #     profile = request.user.customerprofile_user
    #     if profile.business_logo:
    #         profile.business_logo.delete()
    #     else:
    #         return Response(
    #             {
    #                 "success": False,
    #                 "errors": {
    #                     "business_logo": "Can't delete field that is already null"
    #                 },
    #             },
    #             status=status.HTTP_200_OK,
    #         )
    #     return Response(
    #         {"success": True},
    #         status=status.HTTP_200_OK,
    #     )
