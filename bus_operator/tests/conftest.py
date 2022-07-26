from pytest_factoryboy import register
from ..factories import BusOperatorProfileFactory, UserFactory

register(UserFactory, "operator_user", role="BUS_OPERATOR")
register(UserFactory, "user",)
register(BusOperatorProfileFactory, "unapproved_operator")

