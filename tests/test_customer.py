import pytest
from .factories import *
from bus_operator.models import Ticket
from django.urls import reverse


class TestCustomer:
    @pytest.mark.django_db
    def test_bus_ticket_booking(self, api_client, bus_with_stops, customer):
        # Get stop objects from bus
        print(bus_with_stops.busstoppage_bus.all().values("count"))
        stop1 = bus_with_stops.busstoppage_bus.get(count=1)
        stop2 = bus_with_stops.busstoppage_bus.get(count=2)
        stop3 = bus_with_stops.busstoppage_bus.get(count=3)

        # Set Capacity for Bus
        bus_with_stops.capacity = 7
        bus_with_stops.save()

        # Authenticate User for API access
        api_client.force_authenticate(user=customer.user)

        # Book Ticket for stops 1 to 3 with 5 seats
        data = {
            "bus": bus_with_stops.id,
            "journey_date": "2022-07-22",
            "start_bus_stop": stop1.id,
            "end_bus_stop": stop3.id,
            "seats": 5,
            "number": "A303",
        }
        response = api_client.post(reverse("tickets"), data=data, format="json")
        json = response.json()
        print(json)
        assert response.status_code == 201
        assert json["success"] == True

        # Check that bus capacity should not be updated without making successful payment
        assert bus_with_stops.get_available_capacity_stops(1, 3) == 7
        assert "data" in json
        print(json["data"])

        # Make Ticket Payment successful to secure seats reservation
        ticket_id = json["data"]["id"]
        updated = Ticket.objects.filter(id=ticket_id).update(
            payment_status="SUCCESSFUL"
        )
        assert updated == 1

        # Check that bus capacity should be updated after successful payment
        assert bus_with_stops.get_available_capacity_stops(1, 3) == 2

        # Check that bus capacity for stop 1 to 2 should also be 2
        assert bus_with_stops.get_available_capacity_stops(1, 2) == 2

        # Book Ticket For stops 1 to 2 for 2 available seats
        data = {
            "bus": bus_with_stops.id,
            "journey_date": "2022-07-22",
            "start_bus_stop": stop1.id,
            "end_bus_stop": stop2.id,
            "seats": 2,
            "number": "A303",
        }
        response = api_client.post(reverse("tickets"), data=data, format="json")
        json = response.json()
        print(json)
        assert response.status_code == 201
        assert json["success"] == True

        # Make Ticket Payment successful to secure seats reservation
        ticket_id = json["data"]["id"]
        updated = Ticket.objects.filter(id=ticket_id).update(
            payment_status="SUCCESSFUL"
        )
        assert updated == 1

        # Check that bus capacity should 0 for stops 1 to 2 after making successful payment
        assert bus_with_stops.get_available_capacity_stops(1, 2) == 0
        # Check that bus capacity should 2 for stops 2 to 3
        assert bus_with_stops.get_available_capacity_stops(2, 3) == 2

        # Since not seats is available for stop 1 to 2, then same booking request should fail now
        data = {
            "bus": bus_with_stops.id,
            "journey_date": "2022-07-22",
            "start_bus_stop": stop1.id,
            "end_bus_stop": stop2.id,
            "seats": 1,
            "number": "A303",
        }
        response = api_client.post(reverse("tickets"), data=data, format="json")
        json = response.json()
        print(json)
        assert response.status_code == 400
        assert json["success"] == False

        # Check that 2 bus seats should be vacant for stop 2 to 3
        assert bus_with_stops.get_available_capacity_stops(2, 3) == 2

        # Book Ticket For stops 2 to 3 for 2 seats available.
        data = {
            "bus": bus_with_stops.id,
            "journey_date": "2022-07-22",
            "start_bus_stop": stop2.id,
            "end_bus_stop": stop3.id,
            "seats": 1,
            "number": "A303",
        }
        response = api_client.post(reverse("tickets"), data=data, format="json")
        json = response.json()
        print(json)
        assert response.status_code == 201
        assert json["success"] == True

        # Make Ticket Payment to secure seats reservation
        ticket_id = json["data"]["id"]
        updated = Ticket.objects.filter(id=ticket_id).update(
            payment_status="SUCCESSFUL"
        )
        assert updated == 1

        # Check that bus capacity should be updated after successful payment
        assert bus_with_stops.get_available_capacity_stops(2, 3) == 1
        # assert False
