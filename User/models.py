from djongo import models

ROLE_CHOICES = (("DR", "driver"), ("PL", "police"), ("SY", "security"),
                ("LO", "lot_owner"))


class Roles(models.Model):
    role = models.CharField(primary_key=True,
                            max_length=30,
                            choices=ROLE_CHOICES)
    charge = models.DecimalField(max_digits=8, decimal_places=4)


class Users(models.Model):
    _id = models.ObjectIdField()
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=100)
    objects = models.DjongoManager()

    def __str__(self):
        return str(self._id)
