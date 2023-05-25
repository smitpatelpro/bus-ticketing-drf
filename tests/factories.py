import factory
from django.contrib.auth import get_user_model
import datetime

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
    user = factory.SubFactory(UserFactory)
    business_name = factory.faker.Faker("name")
    approval_status = "PENDING_APPROVAL"

    class Meta:
        model = "bus_operator.BusOperatorProfile"


class BusFactory(BaseFactory):
    name = factory.Sequence(lambda n: f"TestBus-{n}")
    operator = factory.SubFactory(
        BusOperatorProfileFactory
    )
    per_km_fare = 7
    capacity = 30
    type = "REGULAR"

    class Meta:
        model = "bus_operator.Bus"


class BusStopFactory(BaseFactory):
    bus = factory.SubFactory(BusFactory)
    name = factory.Iterator(["Ahmedabad", "Udaypur", "Jodhpur", "Jaipur", "Delhi", "Kanpur"])
    arrival_time = factory.LazyFunction(datetime.datetime.now)
    departure_time = factory.LazyFunction(datetime.datetime.now)
    count = factory.Sequence(lambda n: n+1)
    distance_from_last_stop = factory.Sequence(lambda n: n*10)
    journey_type = "UP" # TODO: no longer used. will be removed
    class Meta:
        model = "bus_operator.BusStoppage"


class BusUnavailabilityFactory(BaseFactory):
    bus = factory.SubFactory(BusFactory)

    class Meta:
        model = "bus_operator.BusUnavailability"


# ============ Customer =======================


class CustomerProfileFactory(BaseFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = "customer.CustomerProfile"


class TicketFactory(BaseFactory):
    customer = factory.SubFactory(CustomerProfileFactory)
    bus = factory.SubFactory("bus_operator.tests.factories.BusFactory")

    class Meta:
        model = "bus_operator.Ticket"
