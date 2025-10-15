from django.contrib import admin
from .models import RentalCar

@admin.register(RentalCar)
class RentalCarAdmin(admin.ModelAdmin):
    list_display = ("car_name", "company", "seat_capacity", "fuel_type", "transmission_type", "rating")
    list_filter = ("seat_capacity", "fuel_type", "transmission_type", "rating")
    search_fields = ("car_name", "company")
