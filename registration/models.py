from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (("DR", "driver"), ("PL", "police"), ("SY", "security"),
                ("LO", "lot_owner"))


class Roles(models.Model):
    role = models.CharField(primary_key=True,
                            max_length=30,
                            choices=ROLE_CHOICES)
    charge = models.DecimalField(max_digits=8, decimal_places=4)


class User(AbstractUser):
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
