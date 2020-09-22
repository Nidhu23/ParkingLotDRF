from django.shortcuts import render
from rest_framework import request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from ParkingLot.decorators import jwt_decode, role_required
from parking.models import Parking
from .serializers import VehicleSerializer
# Create your views here.


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
        return Response("error")


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
        return Response("Error")


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
        return Response("Error")