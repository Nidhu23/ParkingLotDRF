from parking.models import Parking
from rest_framework import serializers


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['vehicle_num','vehicle_color','vehicle_type','slot']


