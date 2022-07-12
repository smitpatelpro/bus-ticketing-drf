from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings

v1_base = settings.API_V1_URL_PREFIX

urlpatterns = [
    path(v1_base + 'login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(v1_base + 'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]