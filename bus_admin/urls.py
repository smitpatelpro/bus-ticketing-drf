from django.urls import path
from .views import TestApiView
from django.conf import settings

v1_base = settings.API_V1_URL_PREFIX

urlpatterns = [
    path(v1_base + "test", TestApiView.as_view()),
]
