from django.urls import path
from . import views
from django.conf import settings

v1_base = settings.API_V1_URL_PREFIX

urlpatterns = [
    path(v1_base + "customers/profile", views.ProfileDetailView.as_view(), name="customer-profile"),
    path(v1_base + "customers/profile/media", views.ProfileMediaView.as_view(), name="customer-profile-media"),
    path(v1_base + "customers", views.CustomerProfileView.as_view(), name="customers"),
    path(v1_base + "customers/<uuid>", views.CustomerProfileView.as_view(), name="customer"),
    path(v1_base + "tickets", views.TicketView.as_view(), name="tickets"),
    path(v1_base + "tickets/<uuid>", views.TicketView.as_view(), name="ticket"),
]
