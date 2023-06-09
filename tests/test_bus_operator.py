import pytest
from django.urls import reverse
from .factories import *

bus_data = {
            "name": "Ahmedabad-Kerala-Express",
            "type": "REGULAR",
            "capacity": 80,
            "per_km_fare": "7.00",
        }

class TestBusOperatorProfile:
    @pytest.mark.django_db
    def test_bus_create_access_control_success(self, api_client, approved_operator):
        # For Approved Bus Operator
        api_client.force_authenticate(user=approved_operator.user)
        response = api_client.post(reverse("buses"), data=bus_data, format="json")
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_bus_create_access_control_failure(self, api_client, unapproved_operator):
        # For Unapproved Bus Operator
        api_client.force_authenticate(user=unapproved_operator.user)
        response = api_client.get(reverse("buses"), data=bus_data, format="json")
        assert response.status_code == 403


class TestBus:
    @pytest.mark.django_db
    def test_bus_search_forward_journey(self, api_client, bus_with_stops):
        # Forward Journey Search
        BusStopFactory.reset_sequence(0)
        search_params = {
            "date": "22-07-2022",
            "from": "Ahmedabad",
            "to": "Jaipur",
        }
        response = api_client.get(reverse("buses-search"), data=search_params)
        assert response.status_code == 200
        print(response.json())
        data = response.json()["results"]
        assert len(data) == 1   # It should return only 1 bus which is setup in fixture bus_with_stops
        assert data[0]["id"] == bus_with_stops.id

    @pytest.mark.django_db
    def test_bus_search_reverse_journey(self, api_client, bus_with_stops):
        BusStopFactory.reset_sequence(0)
        # Reverse Journey Search
        search_params = {
            "date": "22-07-2022",
            "from": "Jaipur",
            "to": "Ahmedabad",
        }
        response = api_client.get(reverse("buses-search"), data=search_params)
        assert response.status_code == 200
        print(response.json())
        data = response.json()["results"]
        assert len(data) == 1
        assert data[0]["id"] == bus_with_stops.id

    @pytest.mark.django_db
    def test_bus_unavailability(self, api_client, bus_with_stops):
        # Register bus unavaiability for date 22/07/2022
        BusStopFactory.reset_sequence(0)
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
        data = response.json()["results"]

        # Check that bus should not be present in response data
        assert len(data) == 0
