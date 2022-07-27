import pytest
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate
from .factories import *
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

base_url = "/api/v1/"
profile_endpoint = base_url + "bus_operators/profile"
operators_endpoint = base_url + "bus_operators"
operator_details_endpoint = base_url + "bus_operators/{}"
buses_endpoint = base_url + "buses"
buses_search_endpoint = base_url + "buses/search"
bus_stops_endpoint = base_url + "buses/{}/stops"
bus_stops_details_endpoint = base_url + "buses/{}/stops/{}"


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class TestBusOperatorProfile:
    # endpoint = 'http://localhost:8080/api/v1/bus_operators/profile'

    # @pytest.mark.django_db
    # def test_access(self, request_client, api_client):
    #     user = OperatorUserFactory()
    #     operator = ApprovedBusOperatorProfileFactory(user=user)
    #     api_client.force_authenticate(user=user)

    #     # Test Get
    #     response = api_client.get(self.endpoint)
    #     assert response.status_code == 200

    #     data = {
    #         "full_name": "Smit Patel",
    #         "phone_number": "1234567890",
    #         "business_name": "SP Bus",
    #         "office_address": "test address",
    #         "ratings": 6,
    #     }
    #     # Test_Post
    #     response = api_client.patch(self.endpoint, data=data, format='json')
    #     print(response.json())
    #     assert response.status_code == 200

    # '''
    # With Request Client
    # '''
    # # tokens = get_tokens_for_user(opeator.user)
    # # request_client.headers.update({'Authorization': 'Bearer {}'.format(tokens["access"])}) # For Request Client
    # # response = request_client.get(self.endpoint)
    # # print(opeator.user.role)
    # # print(response)
    # # print(response.json())
    # # assert response.status_code == 200

    @pytest.mark.django_db
    def test_bus_create_access_control(self, api_client):
        bus_data = {
            "name": "Ahmedabad-Kerala-Express",
            "type": "REGULAR",
            "capacity": 80,
            "per_km_fare": "7.00",
        }
        # For Approved Bus Operator
        user_approved = UserFactory.create(role="BUS_OPERATOR")
        approved_operator = BusOperatorProfileFactory.create(
            user=user_approved, approval_status="APPROVED"
        )
        api_client.force_authenticate(user=user_approved)
        response = api_client.post(buses_endpoint, data=bus_data, format="json")
        assert response.status_code == 201

        # For Unapproved Bus Operator
        api_client.force_authenticate(user=user_approved)
        user_unapproved = UserFactory.create(role="BUS_OPERATOR")
        unapproved_operator = BusOperatorProfileFactory.create(
            user=user_unapproved, approval_status="PENDING_APPROVAL"
        )
        api_client.force_authenticate(user=user_unapproved)
        response = api_client.get(buses_endpoint, data=bus_data, format="json")
        assert response.status_code == 403

    # @pytest.mark.django_db
    # def test_bus_access_control(self, api_client):
    #     assert False


class TestBus:
    @pytest.mark.django_db
    def test_bus_availability(self, api_client):
        # bus_data = {
        #     "name": "Ahmedabad-Kerala-Express",
        #     "type": "REGULAR",
        #     "capacity": 80,
        #     "per_km_fare": "7.00"
        # }
        # # Create Bus using Approved Operator
        # user_approved = UserFactory.create(role="BUS_OPERATOR")
        # approved_operator = BusOperatorProfileFactory.create(user=user_approved, approval_status="APPROVED")
        # api_client.force_authenticate(user=user_approved)
        # response = api_client.post(buses_endpoint, data=bus_data, format='json')
        # assert response.status_code == 201
        # bus_json = response.json()["data"]
        # print("bus: ", bus_json)

        user_approved = UserFactory.create(role="BUS_OPERATOR")
        approved_operator = BusOperatorProfileFactory.create(
            user=user_approved, approval_status="APPROVED"
        )
        api_client.force_authenticate(user=user_approved)

        bus = BusFactory(operator=approved_operator, name="Ahmedabad-Kerala-Express")
        bus_stop1 = BusStopFactory.create(
            bus=bus,
            name="Ahmedabad",
            count=1,
            distance_from_last_stop=0,
            arrival_time="09:00:00",
            departure_time="09:15:00",
        )
        bus_stop2 = BusStopFactory.create(
            bus=bus,
            name="Jaipur",
            count=2,
            distance_from_last_stop=50,
            arrival_time="10:00:00",
            departure_time="10:15:00",
        )
        bus_stop3 = BusStopFactory.create(
            bus=bus,
            name="Delhi",
            count=3,
            distance_from_last_stop=100,
            arrival_time="11:00:00",
            departure_time="11:15:00",
        )
        bus_stop4 = BusStopFactory.create(
            bus=bus,
            name="Delhi",
            count=4,
            distance_from_last_stop=0,
            arrival_time="11:00:00",
            departure_time="11:15:00",
        )
        bus_stop5 = BusStopFactory.create(
            bus=bus,
            name="Jaipur",
            count=5,
            distance_from_last_stop=50,
            arrival_time="11:00:00",
            departure_time="11:15:00",
        )
        bus_stop6 = BusStopFactory.create(
            bus=bus,
            name="Ahmedabad",
            count=6,
            distance_from_last_stop=100,
            arrival_time="11:00:00",
            departure_time="11:15:00",
        )

        # Forward Journey Search
        search_params = {
            "date": "22-07-2022",
            "from": "Ahmedabad",
            "to": "Jaipur",
        }
        response = api_client.get(buses_search_endpoint, data=search_params)
        assert response.status_code == 200
        print(response.json())
        data = response.json()["data"]
        assert len(data) == 1
        assert data[0]["id"] == bus.id

        # Reverse Journey Search
        search_params = {
            "date": "22-07-2022",
            "from": "Jaipur",
            "to": "Ahmedabad",
        }
        response = api_client.get(buses_search_endpoint, data=search_params)
        assert response.status_code == 200
        print(response.json())
        data = response.json()["data"]
        assert len(data) == 1
        assert data[0]["id"] == bus.id
