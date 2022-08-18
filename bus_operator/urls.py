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
        views_profile.BusOperatorProfileView.as_view(),
    ),
    path(v1_base + "bus_operators", views_profile.BusOperatorProfileView.as_view()),
    # For admin only
    # path(
    #     v1_base + "bus_operators/<uuid>/media",
    #     views_profile.BusOperatorProfileMediaView.as_view(),
    # ),
]

# Bus Endpoints
urlpatterns += [
    path(
        v1_base + "buses/search", views_bus.BusSearchView.as_view(), name="buses-search"
    ),
    path(v1_base + "buses/<uuid>", views_bus.BusView.as_view(), name="bus"),
    path(v1_base + "buses", views_bus.BusView.as_view(), name="buses"),
    # Photos
    path(
        v1_base + "buses/<uuid>/photos",
        views_bus.BusPhotosView.as_view(),
        name="bus-photos",
    ),
    path(
        v1_base + "buses/<uuid>/photos/<photo_uuid>",
        views_bus.BusPhotosView.as_view(),
        name="bus-photo",
    ),
    # Amenities
    path(
        v1_base + "buses/<uuid>/amenities",
        views_bus.BusAmenitiesView.as_view(),
        name="bus-amenities",
    ),
    path(
        v1_base + "buses/<uuid>/amenities/<amenity_uuid>",
        views_bus.BusAmenitiesView.as_view(),
        name="bus-amenity",
    ),
    # Bus Stops
    path(
        v1_base + "buses/<uuid>/stops",
        views_bus.BusStoppageView.as_view(),
        name="bus-stops",
    ),
    path(
        v1_base + "buses/<uuid>/stops/<stop_uuid>",
        views_bus.BusStoppageView.as_view(),
        name="bus-stop",
    ),
    # Ticket Bookings
    path(
        v1_base + "bookings/tickets",
        views_bus.TicketView.as_view(),
        name="bookings-tickets",
    ),
]
