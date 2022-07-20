from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from . import models, serializers_bus
from common.serializers import MediaSerializer
from django.utils.decorators import method_decorator
from authentication.permission_classes import *
from django.db.models import Q
from datetime import datetime


class BusListView(APIView):
    """
    List All Bus related to BusOperatorProfile
    """

    permission_classes = [BusOperatorOnly]

    def get(self, request, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        buses = models.Bus.objects.filter(operator=profile)
        serializer = serializers_bus.BusSerializer(buses, many=True)
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


class BusDetailView(APIView):
    """
    Get Details of specific bus
    """

    permission_classes = [BusOperatorOnly]

    def get(self, request, uuid, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
        if not bus:
            return Response(
                {"success": False, "message": "Bus does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = serializers_bus.BusSerializer(bus)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, uuid, *args, **kwargs):
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


# Bus Photos Views
class BusPhotosListView(APIView):
    """
    List View for BusPhotos
    """

    permission_classes = [BusOperatorOnly]

    def get(self, request, uuid, *args, **kwargs):
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

    def post(self, request, uuid, *args, **kwargs):
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


class BusPhotosDetailView(APIView):
    """
    Details View for BusPhotos
    """

    permission_classes = [BusOperatorOnly]

    def delete(self, request, uuid, photo_uuid, *args, **kwargs):
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


# Amenities Views
class BusAmenitiesListView(APIView):
    """
    List View for BusAmenities
    """

    permission_classes = [BusOperatorOnly]

    def get(self, request, uuid, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
        if not bus:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers_bus.BusSerializer(bus)
        return Response(
            {"success": True, "data": serializer.data["amenities"]},
            status=status.HTTP_200_OK,
        )


class BusAmenitiesDetailView(APIView):
    """
    Details View for BusAmenities
    """

    permission_classes = [BusOperatorOnly]

    def delete(self, request, uuid, amenity_uuid, *args, **kwargs):
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

    def post(self, request, uuid, amenity_uuid, *args, **kwargs):
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


# BusStoppage Views
class BusStoppageListView(APIView):
    """
    List View for BusStoppage
    """

    permission_classes = [BusOperatorOnly]

    def get(self, request, uuid, *args, **kwargs):
        profile = request.user.busoperatorprofile_user
        bus = models.Bus.objects.filter(operator=profile, id=uuid).first()
        if not bus:
            return Response(
                {"success": False, "message": "Bus does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        stoppages = bus.busstoppage_bus.all()
        serializer = serializers_bus.BusStoppageSerializer(stoppages, many=True)
        return Response(
            {"success": True, "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request, uuid, *args, **kwargs):
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


class BusStoppageDetailView(APIView):
    """
    Get Details of specific bus
    """

    permission_classes = [BusOperatorOnly]

    def get(self, request, uuid, stop_uuid, *args, **kwargs):
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
        serializer = serializers_bus.BusStoppageSerializer(stop)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, uuid, stop_uuid, *args, **kwargs):
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

    def delete(self, request, uuid, stop_uuid, *args, **kwargs):
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


class BusSearchView(APIView):
    """
    It facilitate Searching and Sorting of Buses based on input parameters
    """

    permission_classes = [CustomerOnly]

    def get(self, request, *args, **kwargs):
        from_place = request.GET.get("from")
        to_place = request.GET.get("to")

        departure_start_time = request.GET.get("departure_start_time")
        departure_end_time = request.GET.get("departure_end_time")
        operator = request.GET.get("operator")
        type = request.GET.getlist("type")
        amenities = request.GET.getlist("amenities")
        order_by = request.GET.getlist("order_by")
        # print("amenities:",amenities)

        # stoppages = models.BusStoppage.objects.filter(Q(name__unaccent__icontains=from_place) | Q(name__unaccent__icontains=to_place)).values_list("bus", flat=True) # will works only for Postgresql
        stoppages = models.BusStoppage.objects.filter(
            Q(name__icontains=from_place) | Q(name__icontains=to_place)
        )
        # print("before filter:",stoppages )

        # Filter
        format = "%H:%M:%S"
        if departure_start_time:
            departure_start_time = datetime.strptime(
                departure_start_time, format
            ).time()
            # print("departure_start_time",departure_start_time)
            stoppages = stoppages.exclude(
                Q(departure_time__lt=departure_start_time)
                & Q(name__icontains=from_place)
            )
        if departure_end_time:
            departure_end_time = datetime.strptime(departure_end_time, format).time()
            # print("departure_end_time",departure_end_time)
            stoppages = stoppages.exclude(
                Q(departure_time__gt=departure_end_time) & Q(name__icontains=from_place)
            )

        # print("after filter:",stoppages )
        bus_ids = stoppages.values_list("bus", flat=True).distinct()
        # print(bus_ids)
        bus_list = []
        for bus_id in bus_ids:
            from_stop = stoppages.filter(name__icontains=from_place, bus=bus_id).first()
            to_stop = stoppages.filter(name__icontains=to_place, bus=bus_id).last()
            if from_stop and to_stop and from_stop.count < to_stop.count:
                bus_list.append(bus_id)

            # from_stop = stoppages.filter(name__icontains=from_place, bus=bus_id, journey_type="DOWN").first()
            # to_stop = stoppages.filter(name__icontains=to_place, bus=bus_id, journey_type="DOWN").last()
            # if from_stop and to_stop and from_stop.count > to_stop.count:
            #    bus_list.append(bus_id)

        buses = models.Bus.objects.filter(id__in=bus_list)
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
