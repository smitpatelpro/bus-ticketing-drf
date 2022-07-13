from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

# Create your views here.
class ProfileView(APIView):
    """
    this View is responsible to operate on user profile for currently loggedin user
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        List all objects
        """
        return Response({"Hello": "ProfileView"}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        List all objects
        """
        return Response({"Hello": "ProfileView"}, status=status.HTTP_200_OK)
