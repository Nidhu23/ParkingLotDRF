from django.contrib import admin
from .models import Users
from .models import Roles
# Register your models here.
admin.site.register(Users)
admin.site.register(Roles)