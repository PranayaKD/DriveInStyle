from django.db import models

FUEL_CHOICES = [
    ("Petrol", "Petrol"),
    ("Diesel", "Diesel"),
    ("CNG", "CNG"),
    ("EV", "EV"),
]

SEAT_CHOICES = [
    (5, "5 Seater"),
    (7, "7 Seater"),
]

TRANSMISSION_CHOICES = [
    ("Manual", "Manual"),
    ("Automatic", "Automatic"),
]

RATING_CHOICES = [
    ("3/5", "3/5"),
    ("4/5", "4/5"),
    ("5/5", "5/5"),
]

class RentalCar(models.Model):
    car_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    milage = models.FloatField(help_text="Mileage (km per litre)")
    seat_capacity = models.IntegerField(choices=SEAT_CHOICES)
    transmission_type = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    total_km_driven = models.PositiveIntegerField()
    amenities = models.TextField()
    bootspace = models.CharField(max_length=50)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    car_img = models.ImageField(upload_to="carimg/")

    def __str__(self):
        return f"{self.company} {self.car_name} ({self.seat_capacity} Seater)"
