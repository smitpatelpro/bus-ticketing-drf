from django.urls import path
from . import views
from django.conf import settings

v1_base = settings.API_V1_URL_PREFIX

urlpatterns = [
    path(v1_base + "customers", views.CustomerProfileListView.as_view()),
]
