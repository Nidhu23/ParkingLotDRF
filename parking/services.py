from django.utils import timezone
from .models import UnPark
import jwt
from ParkingLot import settings


def un_park(instance):
    slot = instance.slot
    vehicle_num = instance.vehicle_num
    entry_time = instance.entry_time
    exit_time = timezone.now()
    charge = calc_charge(exit_time, instance)
    un_parked = UnPark.objects.create(charge=charge,
                                      slot=slot,
                                      entry_time=entry_time,
                                      exit_time=exit_time,
                                      vehicle_num=vehicle_num)
    un_parked.save()
    instance.delete()


def calc_charge(exit_time, instance):
    total_parked_time = (exit_time - instance.entry_time)
    total_hours = total_parked_time.total_seconds() / 3600
    if total_hours < 1:
        total_hours = 1
    charges = total_hours * (float(instance.vehicle_type.charge) + float(
        instance.park_type.charge) + float(instance.user.role.charge))
    if instance.disabled:
        DISCOUNT = 0.1
        charges = charges - (charges * DISCOUNT)
    return charges


def get_user(user_token):
    payload = jwt.decode(user_token, settings.SECRET_KEY)
    username = payload.get('username')
    return username
