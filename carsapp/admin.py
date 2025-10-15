from django.contrib import admin
from carsapp.models import Company, Products, ProductInteriorImgs, ProductExteriorImgs,Book_Test_Drive
# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'ceo', 'est_year', 'origin'] 
   

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['product_name',"color","seat_capacity","fuel_type", "cc","milige",'Company',]  
    
class ProductInteriorImgsAdmin(admin.ModelAdmin):
    list_display = ["interior",'product']
    
class ProductExteriorImgsAdmin(admin.ModelAdmin):
    list_display = ["exterior",'product']
   
admin.site.register(Company, CompanyAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductInteriorImgs, ProductInteriorImgsAdmin)
admin.site.register(ProductExteriorImgs, ProductExteriorImgsAdmin)
admin.site.register(Book_Test_Drive)





