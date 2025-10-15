from django.db import models
from btmapp.models import UserRegisteration

# Companies
class Company(models.Model):
    name = models.CharField(max_length=50)
    ceo = models.CharField(max_length=50)
    est_year = models.IntegerField()
    origin = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="logos", blank=True, null=True)

    def __str__(self):
        return self.name

# Products
class Products(models.Model):
    product_name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    seat_capacity = models.IntegerField()
    fuel_type = models.CharField(max_length=100)
    cc = models.IntegerField()
    milige = models.IntegerField()
    price = models.IntegerField()
    prod_image = models.ImageField(upload_to="products", blank=True, null=True)
    Company = models.ForeignKey(Company, related_name="companies", on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

# Product Images
class ProductInteriorImgs(models.Model):
    interior = models.ImageField(upload_to="interior", blank=True, null=True)
    product = models.ForeignKey(Products, related_name='interior_images', on_delete=models.CASCADE)

class ProductExteriorImgs(models.Model):
    exterior = models.ImageField(upload_to="exterior", blank=True, null=True)
    product = models.ForeignKey(Products, related_name='exterior_images', on_delete=models.CASCADE)

# Test Drive Booking
class Book_Test_Drive(models.Model):
    product_name = models.ForeignKey(Products, related_name='booked_test_drives', on_delete=models.CASCADE)
    user = models.ForeignKey(UserRegisteration, on_delete=models.CASCADE)
    t_date = models.DateField()
    time_slot = models.CharField(max_length=50)

# Enquiry
class Enquiry(models.Model):
    user = models.ForeignKey(UserRegisteration, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry from {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"
