from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from registration.models import User
# Create your models here.
park_type_choices = (("Vallet", "Vallet"), ("Own", "Own"))
vehicle_type_choices = (("bike", "bike"), ("car", "car"))


class ParkingType(models.Model):
    park_type = models.CharField(primary_key=True,
                                 max_length=30,
                                 choices=park_type_choices)
    charge = models.DecimalField(max_digits=8, decimal_places=4)


class VehicleType(models.Model):
    vehicle_type = models.CharField(primary_key=True,
                                    max_length=40,
                                    choices=vehicle_type_choices)
    charge = models.DecimalField(max_digits=8, decimal_places=4)


class Parking(models.Model):
    slot = models.IntegerField(
        unique=True, validators=[MaxValueValidator(400),
                                 MinValueValidator(1)])
    vehicle_num = models.CharField(max_length=200, unique=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    park_type = models.ForeignKey(ParkingType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_color = models.CharField(max_length=300)
    disabled = models.BooleanField(choices=((True, True), (False, False)))
    entry_time = models.DateTimeField(auto_now_add=True)

    def assign_slot(self, slots_taken):
        total_slots = set(range(1, 401))
        slot = list(total_slots.difference(slots_taken))
        return slot[0]


class UnPark(models.Model):
    unpark_id = models.AutoField(auto_created=True, primary_key=True)
    slot = models.IntegerField()
    vehicle_num = models.CharField(max_length=200)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(auto_now_add=True)

