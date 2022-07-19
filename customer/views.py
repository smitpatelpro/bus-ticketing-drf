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
