from django.urls import path
from . import views

urlpatterns = [
    path("", views.rental_home, name="rental_home"),
    path("<int:seat_capacity>/", views.rental_list, name="rental_list"),
    path("detail/<int:car_id>/", views.rental_detail, name="rental_details"),
    path("rent/<int:car_id>/", views.rent_now, name="rent_now"),
    path("calculate/<int:car_id>/", views.calculate_rent, name="calculate_rent"),
    path("final_price/<int:car_id>/", views.final_rent_price, name="final_rent_price"),
]
