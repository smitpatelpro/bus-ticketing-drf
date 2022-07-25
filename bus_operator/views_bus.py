from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from . import models, serializers_bus
from common.serializers import MediaSerializer
from django.utils.decorators import method_decorator
from authentication.permission_classes import *
from django.db.models import Q, F
from datetime import datetime
from django.db.models import Case, When, IntegerField, Count, OuterRef, Subquery


class BusView(APIView):
    """
    List All Bus related to BusOperatorProfile
    """

    permission_classes = [BusOperatorOnly]

    def get(self, request, uuid=None, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        if uuid:
            buses = models.Bus.objects.filter(operator=profile, id=uuid).first()
            if not buses:
                return Response(
                    {"success": False, "message": "Bus does not exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            many = False
        else:
            buses = models.Bus.objects.filter(operator=profile)
            many = True
        serializer = serializers_bus.BusSerializer(buses, many=many)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        serializer = serializers_bus.BusSerializer(
            data=request.data, context={"profile": profile}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    def patch(self, request, uuid=None, *args, **kwargs):
        if uuid:
            profile = request.user.busoperatorprofile_user
            bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
            if not bus:
                return Response(
                    {"success": False, "message": "Bus does not exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = serializers_bus.BusSerializer(bus, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
                )
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"success": False, "message": "PATCH is not permitted on collection"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# TODO: Try to combine list and details
# Bus Photos Views
class BusPhotosView(APIView):
    """
    List View for BusPhotos
    """

    permission_classes = [BusOperatorOnly]

    def get(self, request, uuid, photo_uuid=None, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
        if not bus:
            return Response(
                {"success": False, "message": "Bus does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = serializers_bus.BusSerializer(bus)
        return Response(
            {"success": True, "data": serializer.data["photos"]},
            status=status.HTTP_200_OK,
        )

    def post(self, request, uuid, photo_uuid=None, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
        if not bus:
            return Response(
                {"success": False, "message": "Bus does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = MediaSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            media = serializer.save()
            bus.photos.add(media)
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, uuid, photo_uuid=None, *args, **kwargs):
        if photo_uuid: 
            profile = request.user.busoperatorprofile_user
            bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
            if not bus:
                return Response(
                    {"success": False, "message": "Bus does not exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            photo = bus.photos.filter(id=photo_uuid)
            if not photo:
                return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
            photo.delete()
            return Response(
                {"success": True},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"success": False, "message": "DELETE is not permitted on collection"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Amenities Views
class BusAmenitiesView(APIView):
    """
    List View for BusAmenities
    """

    permission_classes = [BusOperatorOnly]

    def get(self, request, uuid, amenity_uuid=None, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
        if not bus:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers_bus.BusSerializer(bus)
        return Response(
            {"success": True, "data": serializer.data["amenities"]},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, uuid, amenity_uuid=None, *args, **kwargs):
        if amenity_uuid:
            profile = request.user.busoperatorprofile_user
            bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
            if not bus:
                return Response(
                    {"success": False, "message": "Bus does not exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            amenity = bus.amenities.filter(id=amenity_uuid)
            if not amenity:
                return Response(
                    {"success": False, "message": "Amenity does not exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            bus.amenities.remove(amenity_uuid)
            return Response(
                {"success": True},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"success": False, "message": "DELETE is not permitted on collection"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request, uuid, amenity_uuid=None, *args, **kwargs):
        if amenity_uuid:
            profile = request.user.busoperatorprofile_user
            bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
            if not bus:
                return Response(
                    {"success": False, "message": "Bus does not exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            amenity = models.BusAmenity.objects.filter(id=amenity_uuid).last()
            bus.amenities.add(amenity)
            return Response(
                {"success": True},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"success": False, "message": "POST is not permitted on this collection"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# BusStoppage Views
class BusStoppageView(APIView):
    """
    List View for BusStoppage
    """

    permission_classes = [BusOperatorOnly]

    def get(self, request, uuid, stop_uuid=None, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
        if not bus:
            return Response(
                {"success": False, "message": "Bus does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        if stop_uuid:
            stoppages = bus.busstoppage_bus.filter(id=stop_uuid).last()
            if not stoppages:
                return Response(
                    {"success": False, "message": "Bus Stop does not exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            many = False
        else:
            stoppages = bus.busstoppage_bus.all()
            many = True
        serializer = serializers_bus.BusStoppageSerializer(stoppages, many=many)
        return Response(
            {"success": True, "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request, uuid, stop_uuid=None, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
        if not bus:
            return Response(
                {"success": False, "message": "Bus does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        request.data["bus"] = bus.id  # Take and overwrite Bus id from URL parameter
        serializer = serializers_bus.BusStoppageSerializer(data=request.data)
        if serializer.is_valid():
            stoppage = serializer.save()
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    # views with stop id
    def patch(self, request, uuid, stop_uuid=None, *args, **kwargs):
        if stop_uuid:
            profile = request.user.busoperatorprofile_user
            bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
            if not bus:
                return Response(
                    {"success": False, "message": "Bus does not exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            stop = bus.busstoppage_bus.filter(id=stop_uuid).last()
            if not stop:
                return Response(
                    {"success": False, "message": "Bus Stop does not exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = serializers_bus.BusStoppageSerializer(
                stop, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
                )
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"success": False, "message": "PATCH is not permitted on this collection"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, uuid, stop_uuid=None, *args, **kwargs):
        if stop_uuid:
            profile = request.user.busoperatorprofile_user
            bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
            if not bus:
                return Response(
                    {"success": False, "message": "Bus does not exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            stop = bus.busstoppage_bus.filter(id=stop_uuid).last()
            if not stop:
                return Response(
                    {"success": False, "message": "Bus Stop does not exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            stop.delete()
            return Response(
                {"success": True},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"success": False, "message": "DELETE is not permitted on this collection"},
                status=status.HTTP_400_BAD_REQUEST,
            )



# # BusJourney Views
# class BusJourneyView(APIView):
#     """
#     List View for BusJourney
#     """

#     permission_classes = [BusOperatorOnly]

#     def get(self, request, uuid, stop_uuid=None, *args, **kwargs):
#         profile = request.user.busoperatorprofile_user
#         bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
#         if not bus:
#             return Response(
#                 {"success": False, "message": "Bus does not exists"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
        
#         if stop_uuid:
#             stoppages = bus.busjourney_bus.filter(id=stop_uuid).last()
#             if not stoppages:
#                 return Response(
#                     {"success": False, "message": "Bus Stop does not exists"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#             many = False
#         else:
#             stoppages = bus.busjourney_bus.all()
#             many = True
#         serializer = serializers_bus.BusStoppageSerializer(stoppages, many=many)
#         return Response(
#             {"success": True, "data": serializer.data},
#             status=status.HTTP_200_OK,
#         )

#     def post(self, request, uuid, stop_uuid=None, *args, **kwargs):
#         profile = request.user.busoperatorprofile_user
#         bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
#         if not bus:
#             return Response(
#                 {"success": False, "message": "Bus does not exists"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         request.data["bus"] = bus.id  # Take and overwrite Bus id from URL parameter
#         serializer = serializers_bus.BusStoppageSerializer(data=request.data)
#         if serializer.is_valid():
#             stoppage = serializer.save()
#             return Response(
#                 {"success": True, "data": serializer.data},
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(
#             {"success": False, "errors": serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST,
#         )
    
#     # views with stop id
#     def patch(self, request, uuid, stop_uuid=None, *args, **kwargs):
#         if stop_uuid:
#             profile = request.user.busoperatorprofile_user
#             bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
#             if not bus:
#                 return Response(
#                     {"success": False, "message": "Bus does not exists"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#             stop = bus.busstoppage_bus.filter(id=stop_uuid).last()
#             if not stop:
#                 return Response(
#                     {"success": False, "message": "Bus Stop does not exists"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#             serializer = serializers_bus.BusStoppageSerializer(
#                 stop, data=request.data, partial=True
#             )
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(
#                     {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
#                 )
#             return Response(
#                 {"success": False, "errors": serializer.errors},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         else:
#             return Response(
#                 {"success": False, "message": "PATCH is not permitted on this collection"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#     def delete(self, request, uuid, stop_uuid=None, *args, **kwargs):
#         if stop_uuid:
#             profile = request.user.busoperatorprofile_user
#             bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
#             if not bus:
#                 return Response(
#                     {"success": False, "message": "Bus does not exists"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#             stop = bus.busstoppage_bus.filter(id=stop_uuid).last()
#             if not stop:
#                 return Response(
#                     {"success": False, "message": "Bus Stop does not exists"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#             stop.delete()
#             return Response(
#                 {"success": True},
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response(
#                 {"success": False, "message": "DELETE is not permitted on this collection"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )



# TODO: Enhance Performance
class BusSearchView(APIView):
    """
    It facilitate Searching and Sorting of Buses based on input parameters
    """

    # permission_classes = [CustomerOnly]

    def get(self, request, *args, **kwargs):
        # Mandatory
        from_place = request.GET.get("from")
        to_place = request.GET.get("to")
        date = request.GET.get("date")

        date_format = "%d-%m-%Y"
        date = datetime.strptime(date, date_format).date()

        # Optional
        departure_start_time = request.GET.get("departure_start_time")
        departure_end_time = request.GET.get("departure_end_time")
        operator = request.GET.get("operator")
        type = request.GET.getlist("type")
        amenities = request.GET.getlist("amenities")
        order_by = request.GET.getlist("order_by")
        # print("amenities:",amenities)

        buses = models.Bus.objects.prefetch_related("busjourney_bus").filter(Q(busjourney_bus__from_place__icontains=from_place) | Q(busjourney_bus__to_place__icontains=to_place) ).distinct()

        frm = Q(name__icontains=from_place)
        to = Q(name__icontains=to_place)
        from_stoppages = models.BusStoppage.objects.filter(frm)
        to_stoppages = models.BusStoppage.objects.filter(to)
        buses = buses.annotate(
            from_dist = Subquery(from_stoppages.filter(bus=OuterRef("id")).values("count")) 
        ).annotate(
            to_dist = Subquery(to_stoppages.filter(bus=OuterRef("id")).values("count"))
        ).filter(from_dist__isnull=False, to_dist__isnull=False).filter(from_dist__lt=F("to_dist") )

        # print("buses=", buses.values("id", "from_dist", "to_dist"))   
        
        # Filters
        if operator:
            buses = buses.filter(operator=operator)
        if type:
            buses = buses.filter(type__in=type)
        if order_by:
            try:
                # TODO: validate if this has security holes
                buses = buses.order_by(order_by[0])
            except:
                return Response(
                    {"success": False, "message": "Invalid order_by values"},
                    status=status.HTTP_200_OK,
                )
        if amenities:
            buses = buses.filter(amenities__in=amenities)

        serializer = serializers_bus.BusSerializer(buses, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


# Operator Ticket Views
class TicketView(APIView):
    """
    Details View for Specific Ticket objects
    """

    permission_classes = [BusOperatorProfileRequired]

    def get(self, request, *args, **kwargs):
        bus = request.GET.get("bus")
        customer = request.GET.get("customer")
        journey_date = request.GET.get("journey_date")
        date_format = "%d-%m-%Y"
        # journey_date = datetime.strptime(journey_date, date_format).date()

        profile = request.user.busoperatorprofile_user
        tickets = models_operator.Ticket.objects.filter(bus__operator=profile)
        
        if bus:
            tickets = tickets.filter(bus=bus)
        if customer:
            tickets = tickets.filter(customer=customer)
        if journey_date:
            tickets = tickets.filter(journey_date=journey_date)

        serializer = serializers_bus.TicketSerializer(tickets, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


'''
# Reference Code for previous search implementation Experiments

        # buses = models.Bus.objects.filter(busstoppage_bus__name__icontains=from_place).filter(busstoppage_bus__name__icontains=to_place)
        # buses = models.Bus.objects.filter(busstoppage_bus__name__icontains=from_place).filter(busstoppage_bus__name__icontains=to_place)



        # .annotate(d = F("busstoppage_bus__count") - F("busstoppage_bus__count") )

        # fm = stoppages.filter(count=OuterRef('count'),
        # ).exclude(count__lte=OuterRef('count'))

        # stoppages = stoppages.annotate(rank=Subquery(F()))

        # print("before filter:",stoppages.values("bus", "count") )
        # print("before filter:",stoppages.values("bus") )

        ## stoppages = models.BusStoppage.objects.filter(Q(name__unaccent__icontains=from_place) | Q(name__unaccent__icontains=to_place)).values_list("bus", flat=True) # will works only for Postgresql
        # stoppages = models.BusStoppage.objects.filter(
        #     Q(name__icontains=from_place) | Q(name__icontains=to_place)
        # )
        ## print("before filter:",stoppages )

        # # Filter
        # format = "%H:%M:%S"
        # if departure_start_time:
        #     departure_start_time = datetime.strptime(
        #         departure_start_time, format
        #     ).time()
        #     # print("departure_start_time",departure_start_time)
        #     stoppages = stoppages.exclude(
        #         Q(departure_time__lt=departure_start_time)
        #         & Q(name__icontains=from_place)
        #     )
        # if departure_end_time:
        #     departure_end_time = datetime.strptime(departure_end_time, format).time()
        #     # print("departure_end_time",departure_end_time)
        #     stoppages = stoppages.exclude(
        #         Q(departure_time__gt=departure_end_time) & Q(name__icontains=from_place)
        #     )

        # # print("after filter:",stoppages )
        # bus_ids = stoppages.values_list("bus", flat=True).distinct()
        # # print(bus_ids)
        # bus_list = []

        # # TODO: Make distance as absolute and optimize performance by removing looping over queryset
        # for bus_id in bus_ids:
        #     from_stop = stoppages.filter(name__icontains=from_place, bus=bus_id).first()
        #     to_stop = stoppages.filter(name__icontains=to_place, bus=bus_id).last()
        #     if from_stop and to_stop and from_stop.count < to_stop.count:
        #         bus_list.append(bus_id)

        #     # from_stop = stoppages.filter(name__icontains=from_place, bus=bus_id, journey_type="DOWN").first()
        #     # to_stop = stoppages.filter(name__icontains=to_place, bus=bus_id, journey_type="DOWN").last()
        #     # if from_stop and to_stop and from_stop.count > to_stop.count:
        #     #    bus_list.append(bus_id)

        # buses = models.Bus.objects.filter(id__in=bus_list)
        # buses = models.Bus.objects.filter(id__in=bus_ids)

        # buses = models.Bus.objects.prefetch_related("busstoppage_bus").filter(busstoppage_bus__name__icontains=from_place).filter(busstoppage_bus__name__icontains=to_place).distinct()

        # buses = models.Bus.objects.prefetch_related("busjourney_bus").filter(busjourney_bus__from_place__icontains=from_place, busjourney_bus__to_place__icontains=to_place).distinct()
        # buses = models.Bus.objects.prefetch_related("busjourney_bus").filter(Q(busjourney_bus__from_place__icontains=from_place) | Q(busjourney_bus__to_place__icontains=to_place) ).distinct()
        # buses = models.Bus.objects.prefetch_related("busjourney_bus").filter(Q(busjourney_bus__from_place__icontains=from_place) | Q(busjourney_bus__to_place__icontains=to_place) ).distinct()

        # buses = models.Bus.objects.prefetch_related("busjourney_bus")

        # or p in Person.objects.raw('SELECT * FROM myapp_person'):
        """
        TODO:
        Run Raw Query 
        SELECT s1.*, s2.* FROM bus_operator_busstoppage as s1 INNER JOIN bus_operator_busstoppage as s2 ON s1.bus_id = s2.bus_id 
        WHERE lower(s1.name) = "ahmedabad" and lower(s2.name)="jaipur"
        and s1.distance_from_last_stop < s2.distance_from_last_stop; 
        """
        query = """SELECT s1.*, s2.* FROM bus_operator_busstoppage as s1 INNER JOIN bus_operator_busstoppage as s2 ON s1.bus_id = s2.bus_id 
        WHERE lower(s1.name) = %s and lower(s2.name)=%s
        and s1.distance_from_last_stop < s2.distance_from_last_stop"""
        
        # buses = models.Bus.objects.raw(query, [from_place, to_place])

        # print(buses.values("id"))
        # for bus in buses:
            # if bus.id in 
        # # TODO: Validate Performance
        # buses = models.Bus.objects.filter(Q(busjourney_bus__from_place__icontains=from_place) | Q(busjourney_bus__to_place__icontains=to_place) )
        # # buses = models.Bus.objects.all()
        # buses = buses.annotate(
        #     from_count=Count(
        #         Case(
        #             When(busjourney_bus__from_place__icontains=from_place, then=1),
        #             output_field=IntegerField(),
        #         )
        #     )
        # )
        # buses = buses.annotate(
        #     to_count=Count(
        #         Case(
        #             When(busjourney_bus__to_place__icontains=to_place, then=1),
        #             output_field=IntegerField(),
        #         )
        #     )
        # )

        # # if date in buses.busunavailability_bus.date:
        # buses = buses.filter(from_count__gt=0, to_count__gt=0).exclude(busunavailability_bus__date=date)

        # journeys = models.BusJourney.objects.filter(Q(from_place__icontains=from_place) | Q(to_place__icontains=to_place))
        # bus_ids = journeys.values_list("bus", flat=True).distinct()
        # buses = models.Bus.objects.filter(id__in=bus_ids)

'''