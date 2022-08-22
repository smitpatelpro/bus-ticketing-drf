import factory
from django.contrib.auth import get_user_model

User = get_user_model()

# ============ Base =======================


class BaseFactory(factory.django.DjangoModelFactory):
    id = factory.faker.Faker("uuid4")


# ============ Bus Operator =======================


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


class BusFactory(BaseFactory):
    name = factory.faker.Faker("name")
    operator = factory.SubFactory(
        "bus_operator.tests.factories.BusOperatorProfileFactory"
    )
    per_km_fare = 7
    capacity = 30
    # type = "REGULAR"

    class Meta:
        model = "bus_operator.Bus"


class BusStopFactory(BaseFactory):
    bus = factory.SubFactory("bus_operator.tests.factories.BusFactory")

    class Meta:
        model = "bus_operator.BusStoppage"


class BusUnavailabilityFactory(BaseFactory):
    bus = factory.SubFactory("bus_operator.tests.factories.BusFactory")

    class Meta:
        model = "bus_operator.BusUnavailability"


# ============ Customer =======================


class CustomerProfileFactory(BaseFactory):
    user = factory.SubFactory("bus_operator.tests.factories.UserFactory")
    # gender = "MALE"
    # address = "Test Address"
    # id_proof = None
    # address_proof = None
    # other_kyc_document = None

    class Meta:
        model = "customer.CustomerProfile"


class TicketFactory(BaseFactory):
    customer = factory.SubFactory("bus_operator.tests.factories.CustomerProfileFactory")
    bus = factory.SubFactory("bus_operator.tests.factories.BusFactory")
    # number = "T101"
    # payment_status = "PENDING"

    class Meta:
        model = "bus_operator.Ticket"


"""
=====================================================================
           Removed Code for reference to explain bad design
=====================================================================
NOTE: Don't create specialized class for all types of Users, 
Because all will have duplicated fields. instead of that, 
move that responsibility to fixtures or test cases to create 
proper object with proper filed values and 
create one factory for one model.
=====================================================================

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
"""
