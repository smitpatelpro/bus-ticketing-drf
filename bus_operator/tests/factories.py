import factory
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class BaseFactory(factory.django.DjangoModelFactory):
    id = factory.faker.Faker("uuid4")


class UserFactory(BaseFactory):
    full_name = factory.faker.Faker("name")
    role = "CUSTOMER"
    email = factory.Sequence(lambda n: "person{}@example.com".format(n))

    class Meta:
        model = User
        django_get_or_create = ("email",)


class BusOperatorProfileFactory(BaseFactory):
    user = factory.SubFactory("bus_operator.tests.factories.UserFactory")
    business_name = factory.faker.Faker("name")
    approval_status = "PENDING_APPROVAL"

    class Meta:
        model = "bus_operator.BusOperatorProfile"


# class CustomerUserFactory(factory.django.DjangoModelFactory):
#     id = factory.faker.Faker('uuid4')
#     full_name = factory.faker.Faker('name')
#     role = "CUSTOMER"
#     email = factory.Sequence(lambda n: 'person{}@example.com'.format(n))

#     class Meta:
#         model = User
#         django_get_or_create = ('email',)

# class OperatorUserFactory(factory.django.DjangoModelFactory):
#     id = factory.faker.Faker('uuid4')
#     full_name = factory.faker.Faker('name')
#     role = "BUS_OPERATOR"
#     email = factory.Sequence(lambda n: 'person{}@example.com'.format(n))

#     class Meta:
#         model = User
#         django_get_or_create = ('email',)

# class AdminUserFactory(factory.django.DjangoModelFactory):
#     id = factory.faker.Faker('uuid4')
#     full_name = factory.faker.Faker('name')
#     role = "ADMIN"
#     email = factory.Sequence(lambda n: 'person{}@example.com'.format(n))

#     class Meta:
#         model = User
#         django_get_or_create = ('email',)


# class UnapprovedBusOperatorProfileFactory(factory.django.DjangoModelFactory):
#     user = factory.SubFactory('bus_operator.tests.factories.OperatorUserFactory')
#     business_name = factory.faker.Faker('name')
#     approval_status = "PENDING_APPROVAL"

#     class Meta:
#         model = "bus_operator.BusOperatorProfile"

# class ApprovedBusOperatorProfileFactory(factory.django.DjangoModelFactory):
#     user = factory.SubFactory('bus_operator.tests.factories.OperatorUserFactory')
#     business_name = factory.faker.Faker('name')
#     approval_status = "APPROVED"

#     class Meta:
#         model = "bus_operator.BusOperatorProfile"


class BusFactory(BaseFactory):
    name = factory.faker.Faker("name")
    operator = factory.SubFactory(
        "bus_operator.tests.factories.BusOperatorProfileFactory"
    )
    per_km_fare = 7
    capacity = 30
    type = "REGULAR"

    class Meta:
        model = "bus_operator.Bus"


class BusStopFactory(BaseFactory):
    bus = factory.SubFactory("bus_operator.tests.factories.BusFactory")
    distance_from_last_stop = 100
    journey_type = "UP"

    class Meta:
        model = "bus_operator.BusStoppage"
