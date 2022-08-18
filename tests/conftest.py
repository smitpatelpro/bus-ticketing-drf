import pytest
from .factories import *
from rest_framework.test import APIClient

# # Helper Methods
# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         "refresh": str(refresh),
#         "access": str(refresh.access_token),
#     }

# Fixtures


@pytest.fixture
def api_client():
    return APIClient()


# @pytest.fixture
# def request_client():
#     return RequestsClient()


@pytest.fixture
def customer():
    user = UserFactory.create(role="CUSTOMER")
    customer = CustomerProfileFactory.create(user=user)
    return customer


@pytest.fixture
def unapproved_operator():
    user_unapproved = UserFactory.create(role="BUS_OPERATOR")
    unapproved_operator = BusOperatorProfileFactory.create(
        user=user_unapproved, approval_status="PENDING_APPROVAL"
    )
    return unapproved_operator


@pytest.fixture
def approved_operator():
    user_approved = UserFactory.create(role="BUS_OPERATOR")
    approved_operator = BusOperatorProfileFactory.create(
        user=user_approved, approval_status="APPROVED"
    )
    return approved_operator


@pytest.fixture
def bus_with_stops(api_client, approved_operator):

    api_client.force_authenticate(user=approved_operator.user)
    # api_client.force_authenticate(user=user_approved)
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
    return bus


# register(OperatorUserFactory, "operator_user", role="BUS_OPERATOR")
# register(AdminUserFactory, "admin_user", role="ADMIN")
# # register(CustomerUserFactory, "user")
# register(UnapprovedBusOperatorProfileFactory, "unapproved_operator")
# register(ApprovedBusOperatorProfileFactory, "approved_operator", approval_status="APPROVED")
# register(BusFactory, "buses")
