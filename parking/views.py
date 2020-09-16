from django.shortcuts import render
from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from .serializers import ParkSerializer
from .models import Parking, UnPark
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
#from rest_framework_simplejwt import authentication
# Create your views here.


class Park(APIView):
    def post(self, request):
        try:
            slot_list = set(Parking.objects.values_list("slot", flat=True))
            slot = Parking().assign_slot(slot_list)
            set_slot = Parking()
            setattr(set_slot, 'slot', slot)
            serializer = ParkSerializer(data=request.data, instance=set_slot)
            if serializer.is_valid():
                serializer.save()
                return Response("Your car has been parked",
                                status=status.HTTP_201_CREATED)
        except Parking.DoesNotExist:
            return Response("Park object does not exist")
        except ParseError:
            return Response("Check your request data",
                            status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors)

    def delete(self, request):
        try:
            vehicle_num = request.data.get('vehicle_num')
            park_details = Parking.objects.get(vehicle_num=vehicle_num)
            slot = park_details.slot
            vehicle_num = park_details.vehicle_num
            entry_time = park_details.entry_time
            un_park = UnPark.objects.create(slot=slot,
                                            vehicle_num=vehicle_num,
                                            entry_time=entry_time)
            un_park.save()
            park_details.delete()
            return Response("Unparked", status=status.HTTP_201_CREATED)
        except Parking.DoesNotExist:
            return Response("The vehicle with this number is not parked here",status=status.HTTP_404_NOT_FOUND)
