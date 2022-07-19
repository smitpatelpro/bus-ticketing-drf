from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


# class TestApiView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     # Test View to have protected get endpoint
#     def get(self, request, *args, **kwargs):
#         """
#         List all objects
#         """
#         return Response({"Hello": "World"}, status=status.HTTP_200_OK)
