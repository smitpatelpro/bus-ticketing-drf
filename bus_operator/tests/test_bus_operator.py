import pytest
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate
from .factories import *
# @pytest.mark.django_db
# def test_operator_access(unapproved_operator, operator_user):
#     # print("full_name: ", operator_user.full_name)
#     # print("approval_status", unapproved_operator.approval_status)
#     # # print("name", buses.name)
    

#     assert False
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class TestBusOperatorProfile:
    # endpoint = 'http://localhost:8080/api/v1/bus_operators/profile'
    profile_endpoint = '/api/v1/bus_operators/profile'
    operators_endpoint = '/api/v1/bus_operators'
    operator_details_endpoint = '/api/v1/bus_operators/{}'
    buses_endpoint = '/api/v1/buses'

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
    def test_bus_access_control(self, api_client):
        bus_data = {
            "name": "Ahmedabad-Kerala-Express",
            "type": "REGULAR",
            "capacity": 80,
            "per_km_fare": "7.00"
        }
        # For Approved Bus Operator
        user_approved = UserFactory.create(role="BUS_OPERATOR")
        approved_operator = BusOperatorProfileFactory.create(user=user_approved, approval_status="APPROVED")
        # print(user_approved.__dict__)
        # print(approved_operator.__dict__)
        api_client.force_authenticate(user=user_approved)
        response = api_client.post(self.buses_endpoint, data=bus_data, format='json')
        assert response.status_code == 201

        # For Unapproved Bus Operator
        api_client.force_authenticate(user=user_approved)
        user_unapproved = UserFactory.create(role="BUS_OPERATOR")
        unapproved_operator = BusOperatorProfileFactory.create(user=user_unapproved, approval_status="PENDING_APPROVAL")
        # print(user_unapproved.__dict__)
        # print(unapproved_operator.__dict__)
        api_client.force_authenticate(user=user_unapproved)
        response = api_client.get(self.buses_endpoint, data=bus_data, format='json')
        assert response.status_code == 403
    
    # @pytest.mark.django_db
    # def test_bus_access_control(self, api_client):
    #     assert False