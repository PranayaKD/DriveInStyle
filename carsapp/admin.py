from django.contrib import admin
from .models import Company, Product, ProductInteriorImage, ProductExteriorImage, TestDriveBooking, Enquiry


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'ceo', 'est_year', 'origin']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'color', 'seat_capacity', 'fuel_type', 'cc', 'mileage', 'company']


class ProductInteriorImageAdmin(admin.ModelAdmin):
    list_display = ['interior', 'product']


class ProductExteriorImageAdmin(admin.ModelAdmin):
    list_display = ['exterior', 'product']


class TestDriveBookingAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'booking_date', 'time_slot']
    list_filter = ['booking_date', 'time_slot']


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['phone', 'message']


admin.site.register(Company, CompanyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInteriorImage, ProductInteriorImageAdmin)
admin.site.register(ProductExteriorImage, ProductExteriorImageAdmin)
admin.site.register(TestDriveBooking, TestDriveBookingAdmin)
admin.site.register(Enquiry, EnquiryAdmin)
