import pytest
from .factories import *
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()


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
    bus = BusFactory(operator=approved_operator, name="Ahmedabad-Kanpur-Express")
    BusStopFactory.reset_sequence(0)
    stops = BusStopFactory.create_batch(10, bus=bus)
    print(stops)
    return bus
