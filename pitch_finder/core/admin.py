from django.contrib import admin
from core.models import User, Reservation, Pitch


admin.site.register([User, Reservation, Pitch])
