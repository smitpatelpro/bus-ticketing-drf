from django.urls import path
from . import views_profile, views_bus
from django.conf import settings

v1_base = settings.API_V1_URL_PREFIX

# Profile Endpoints
urlpatterns = [
    path(v1_base + "bus_operators/profile", views_profile.ProfileDetailView.as_view()),
    path(
        v1_base + "bus_operators/profile/media",
        views_profile.ProfileMediaView.as_view(),
    ),
    path(
        v1_base + "bus_operators/<uuid>",
        views_profile.BusOperatorProfileDetailView.as_view(),
    ),
    path(v1_base + "bus_operators", views_profile.BusOperatorProfileListView.as_view()),
    # For admin only
    # path(
    #     v1_base + "bus_operators/<uuid>/media",
    #     views_profile.BusOperatorProfileMediaView.as_view(),
    # ),
]

# Bus Endpoints
urlpatterns += [
    path(v1_base + "buses", views_bus.BusListView.as_view()),
    path(v1_base + "buses/<uuid>", views_bus.BusDetailView.as_view()),
    path(v1_base + "buses/<uuid>/photos", views_bus.BusPhotosListView.as_view()),
    path(
        v1_base + "buses/<uuid>/photos/<photo_uuid>",
        views_bus.BusPhotosDetailView.as_view(),
    ),
    path(v1_base + "buses/<uuid>/amenities", views_bus.BusAmenitiesListView.as_view()),
    path(
        v1_base + "buses/<uuid>/amenities/<amenity_uuid>",
        views_bus.BusAmenitiesDetailView.as_view(),
    ),
]
