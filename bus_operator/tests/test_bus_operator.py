import pytest
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate
from .factories import *
from rest_framework_simplejwt.tokens import RefreshToken

profile_endpoint = '/api/v1/bus_operators/profile'
operators_endpoint = '/api/v1/bus_operators'
operator_details_endpoint = '/api/v1/bus_operators/{}'
buses_endpoint = '/api/v1/buses'
bus_stops_endpoint = '/api/v1/buses/{}/stops'
bus_stops_details_endpoint = '/api/v1/buses/{}/stops/{}'

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
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
            "per_km_fare": "7.00"
        }
        # For Approved Bus Operator
        user_approved = UserFactory.create(role="BUS_OPERATOR")
        approved_operator = BusOperatorProfileFactory.create(user=user_approved, approval_status="APPROVED")
        api_client.force_authenticate(user=user_approved)
        response = api_client.post(buses_endpoint, data=bus_data, format='json')
        assert response.status_code == 201

        # For Unapproved Bus Operator
        api_client.force_authenticate(user=user_approved)
        user_unapproved = UserFactory.create(role="BUS_OPERATOR")
        unapproved_operator = BusOperatorProfileFactory.create(user=user_unapproved, approval_status="PENDING_APPROVAL")
        api_client.force_authenticate(user=user_unapproved)
        response = api_client.get(buses_endpoint, data=bus_data, format='json')
        assert response.status_code == 403
    
    # @pytest.mark.django_db
    # def test_bus_access_control(self, api_client):
    #     assert False



class TestBus:
    
    @pytest.mark.django_db
    def test_bus_availability(self, api_client):
        bus_data = {
            "name": "Ahmedabad-Kerala-Express",
            "type": "REGULAR",
            "capacity": 80,
            "per_km_fare": "7.00"
        }
        # Create Bus using Approved Operator
        user_approved = UserFactory.create(role="BUS_OPERATOR")
        approved_operator = BusOperatorProfileFactory.create(user=user_approved, approval_status="APPROVED")
        api_client.force_authenticate(user=user_approved)
        response = api_client.post(buses_endpoint, data=bus_data, format='json')
        assert response.status_code == 201
        bus_json = response.json()["data"]
        print("bus: ", bus_json)
        
        bus_stop_data = {
            "count": 1,
            "name": "Ahmedabad",
            "arrival_time": "12:00:06",
            "departure_time": "12:50:06",
            "distance": 0,
            "journey_type": "UP"
        }
        response = api_client.post(bus_stops_endpoint.format(bus_json["id"]), data=bus_stop_data, format='json')
        assert response.status_code == 201
        stop1_json = response.json()["data"]
        print("stop1: ", stop1_json)

        bus_stop_data = {
            "count": 2,
            "name": "Ahmedabad",
            "arrival_time": "12:00:06",
            "departure_time": "12:50:06",
            "distance": 0,
            "journey_type": "UP"
        }
        response = api_client.post(bus_stops_endpoint.format(bus_json["id"]), data=bus_stop_data, format='json')
        assert response.status_code == 201
        stop2_json = response.json()["data"]
        print("stop2: ", stop2_json)

        # assert False




       