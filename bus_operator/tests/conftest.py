import pytest
from pytest_factoryboy import register

# from .factories import ( ApprovedBusOperatorProfileFactory, UnapprovedBusOperatorProfileFactory,
#         BusFactory, OperatorUserFactory, AdminUserFactory,  CustomerUserFactory)
from .factories import *
from rest_framework.test import APIClient, RequestsClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def request_client():
    return RequestsClient()


# register(OperatorUserFactory, "operator_user", role="BUS_OPERATOR")
# register(AdminUserFactory, "admin_user", role="ADMIN")
# # register(CustomerUserFactory, "user")
# register(UnapprovedBusOperatorProfileFactory, "unapproved_operator")
# register(ApprovedBusOperatorProfileFactory, "approved_operator", approval_status="APPROVED")
# register(BusFactory, "buses")
