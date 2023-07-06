from django.core.management.base import BaseCommand
from tests.factories import BusFactory, BusStopFactory
import faker
from bus_operator.models import BusOperatorProfile
# from django.contrib.auth import get_user_model
# User = get_user_model()


class Command(BaseCommand):
    help = 'Generate Random Bus Data and store in DB'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Indicates the number of objects to be created')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        print(count)
        operator = BusOperatorProfile.objects.last()
        buses = BusFactory.create_batch(count, operator=operator)
        for bus in buses:
            stops = BusStopFactory.create_batch(10, bus=bus)
            BusStopFactory.reset_sequence(0)
            # bus.save()
        
        # print(buses)
        # print(stops)
        print("Done!")
        