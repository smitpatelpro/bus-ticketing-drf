import factory
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    full_name = "Jon Doe"
    role = "CUSTOMER"
    email = "test@nickelfox.com"

    class Meta:
        model = User
        django_get_or_create = ('email',)


class BusOperatorProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory('bus_operator.tests.factories.UserFactory')
    business_name = "asdasdasd"
    approval_status = "PENDING_APPROVAL"

    class Meta:
        model = "bus_operator.BusOperatorProfile"

class BusFactory(factory.django.DjangoModelFactory):
    operator = factory.SubFactory('bus_operator.tests.factories.BusOperatorProfileFactory')

    class Meta:
        model = "bus_operator.Bus"


from pytest_factoryboy import register
# from .factories import BusOperatorProfileFactory, UserFactory

register(UserFactory, "operator_user", role="BUS_OPERATOR")
register(UserFactory, "user",)
register(BusOperatorProfileFactory, "unapproved_operator")
