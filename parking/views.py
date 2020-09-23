from django.shortcuts import render
from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from .serializers import ParkSerializer
from .models import Parking, UnPark
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
import logging
from ParkingLot.decorators import jwt_decode, role_required
from . import services
logger = logging.getLogger('django')
#from rest_framework_simplejwt import authentication
# Create your views here.


class Park(APIView):

    ''' 
    Park API

    Parameters:
    request paramter: having vehicle details

    Returns:
    parks the vehicle and returns status code
    '''
    @jwt_decode
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
            logger.error("parking object not found")
            return Response("Park object does not exist",status=status.HTTP_404_NOT_FOUND)
        except ParseError:
            return Response("Check your request data",
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    ''' 
    Unpark API

    Parameters:
    request paramter: having vehicle number

    Returns:
    unparks vehicle associated to the vehicle number in the request
    '''
    @jwt_decode
    def delete(self, request):
        try:
            vehicle_num = request.data.get('vehicle_num')
            park_details = Parking.objects.get(vehicle_num=vehicle_num)
            services.un_park(park_details)
            return Response("Unparked", status=status.HTTP_201_CREATED)
        except Parking.DoesNotExist as exception:
            logger.error("parking object not found", exception)
            return Response("The vehicle with this number is not parked here",
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response(ex,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    ''' 
    Search API

    Parameters:
    request paramter: having vehicle number

    Returns:
    details of vehicle associated to the vehicle number in the request
    '''
@api_view(['GET'])
@jwt_decode
@role_required(roles_allowed=["police", "security", "lot_owner"])
def vehicle_num_search(request):
    try:
        vehicle_num = request.data.get('vehicle_num')
        queryset = Parking.objects.filter(vehicle_num=vehicle_num)
        serializer = VehicleSerializer(queryset, many=True)
        if serializer.data == []:
            return Response("vehicle with this number not parked here",
                            status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Parking.DoesNotExist:
        return Response("vehicle with this number is not parked here",
                        status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response("Could not get vehicle details",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    ''' 
    Search API

    Parameters:
    request paramter: having vehicle type

    Returns:
    details of vehicle associated to the vehicle number in the request
    '''
@api_view(['GET'])
@jwt_decode
@role_required(roles_allowed=["police", "security", "lot_owner"])
def vehicle_type_search(request):
    try:
        vehicle_type = request.data.get('vehicle_type')
        queryset = Parking.objects.filter(vehicle_type=vehicle_type)
        serializer = VehicleSerializer(queryset, many=True)
        if serializer.data == []:
            return Response("vehicle of this type not parked here",
                            status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Parking.DoesNotExist:
        return Response("vehicle of this type is not parked here",
                        status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response("Could not get vehicle details",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    ''' 
    Search API

    Parameters:
    request paramter: having vehicle color

    Returns:
    details of vehicle associated to the vehicle color in the request
    '''
@api_view(['GET'])
@jwt_decode
@role_required(roles_allowed=["police", "security", "lot_owner"])
def vehicle_color_search(request):
    try:
        vehicle_color = request.data.get('vehicle_color')
        queryset = Parking.objects.filter(vehicle_color=vehicle_color)
        serializer = VehicleSerializer(queryset, many=True)
        if serializer.data == []:
            return Response("vehicle of this color not parked here",
                            status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Parking.DoesNotExist:
        return Response("vehicle with this color is not parked here",
                        status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response("Could not get vehicle details",status=status.HTTP_500_INTERNAL_SERVER_ERROR)