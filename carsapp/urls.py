from django.urls import path
from . import views

urlpatterns = [
    path("", views.company_list, name="company"),
    path("<int:id>", views.company_details, name="company_details"),
    path("product/<int:id>/", views.product_detail, name="product_detail"),
    path("calcemi/<int:id>", views.calcemi, name="calcemi"),
    path("finalprice/<int:id>", views.final_price, name="product_final_price"),
    path("booktestdrive/<int:id>", views.Book_Test_Drive_views, name="book_test_drive"),
    path("enquiry/", views.make_enquiry, name="make_enquiry"),
]
