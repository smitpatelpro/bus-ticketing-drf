import pytest
from django.urls import reverse
# from rest_framework.test import APIClient
# from rest_framework.test import force_authenticate
from .factories import *
# from .constants import *

# from .conftest import get_tokens_for_user
# from datetime import datetime, timedelta


class TestBusOperatorProfile:

    @pytest.mark.django_db
    def test_bus_create_access_control(
        self, api_client, approved_operator, unapproved_operator
    ):
        bus_data = {
            "name": "Ahmedabad-Kerala-Express",
            "type": "REGULAR",
            "capacity": 80,
            "per_km_fare": "7.00",
        }
        # For Approved Bus Operator
        api_client.force_authenticate(user=approved_operator.user)
        response = api_client.post(reverse("buses"), data=bus_data, format="json")
        assert response.status_code == 201

        # For Unapproved Bus Operator
        api_client.force_authenticate(user=unapproved_operator.user)
        response = api_client.get(reverse("buses"), data=bus_data, format="json")
        assert response.status_code == 403


class TestBus:
    @pytest.mark.django_db
    def test_bus_search(self, api_client, bus_with_stops):
        # Forward Journey Search
        search_params = {
            "date": "22-07-2022",
            "from": "Ahmedabad",
            "to": "Jaipur",
        }
        response = api_client.get(reverse("buses-search"), data=search_params)
        assert response.status_code == 200
        print(response.json())
        data = response.json()["data"]
        assert len(data) == 1
        assert data[0]["id"] == bus_with_stops.id

        # Reverse Journey Search
        search_params = {
            "date": "22-07-2022",
            "from": "Jaipur",
            "to": "Ahmedabad",
        }
        response = api_client.get(reverse("buses-search"), data=search_params)
        assert response.status_code == 200
        print(response.json())
        data = response.json()["data"]
        assert len(data) == 1
        assert data[0]["id"] == bus_with_stops.id

    @pytest.mark.django_db
    def test_bus_unavailability(self, api_client, bus_with_stops):
        # Register bus unavaiability
        BusUnavailabilityFactory.create(bus=bus_with_stops, date="2022-07-22")

        # Forward Journey Search for given bus
        search_params = {
            "date": "22-07-2022",
            "from": "Ahmedabad",
            "to": "Jaipur",
        }
        response = api_client.get(reverse("buses-search"), data=search_params)
        assert response.status_code == 200
        print(response.json())
        data = response.json()["data"]

        # Check that bus should not be present in response data
        assert len(data) == 0
