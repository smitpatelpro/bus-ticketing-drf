from django.urls import path
from . import views
from django.conf import settings

v1_base = settings.API_V1_URL_PREFIX

urlpatterns = [
    path(v1_base + "profile", views.ProfileView.as_view()),
    path(v1_base + "amenities", views.AmenitiesListView.as_view()),
]
