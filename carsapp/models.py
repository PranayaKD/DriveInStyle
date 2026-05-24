from django.db import models
from btmapp.models import UserRegistration


class Company(models.Model):
    name = models.CharField(max_length=50)
    ceo = models.CharField(max_length=50)
    est_year = models.IntegerField()
    origin = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="logos", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    seat_capacity = models.IntegerField()
    fuel_type = models.CharField(max_length=100)
    cc = models.IntegerField()
    mileage = models.IntegerField()
    price = models.IntegerField()
    prod_image = models.ImageField(upload_to="products", blank=True, null=True)
    company = models.ForeignKey(Company, related_name="products", on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class ProductInteriorImage(models.Model):
    interior = models.ImageField(upload_to="interior", blank=True, null=True)
    product = models.ForeignKey(Product, related_name='interior_images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Interior - {self.product.product_name}"


class ProductExteriorImage(models.Model):
    exterior = models.ImageField(upload_to="exterior", blank=True, null=True)
    product = models.ForeignKey(Product, related_name='exterior_images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Exterior - {self.product.product_name}"


class TestDriveBooking(models.Model):
    product = models.ForeignKey(Product, related_name='test_drive_bookings', on_delete=models.CASCADE)
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    booking_date = models.DateField()
    time_slot = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Test Drive Booking"
        verbose_name_plural = "Test Drive Bookings"

    def __str__(self):
        return f"Test Drive: {self.product.product_name} by {self.user.user.username}"


class Enquiry(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"Enquiry from {self.user.user.username} on {self.created_at.strftime('%Y-%m-%d')}"
