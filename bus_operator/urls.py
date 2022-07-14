from django.urls import path
from . import views
from django.conf import settings

v1_base = settings.API_V1_URL_PREFIX

urlpatterns = [
    path(v1_base + "bus_operators", views.BusOperatorProfileListView.as_view()),
    path(
        v1_base + "bus_operators/<uuid>", views.BusOperatorProfileDetailView.as_view()
    ),
    path(
        v1_base + "bus_operators/<uuid>/media",
        views.BusOperatorProfileMediaView.as_view(),
    ),
]
