from django.shortcuts import render, get_object_or_404
from .models import RentalCar
from .services import estimate_rent, calculate_final_rent
from btmapp.utils import send_rental_bill_email
import logging

logger = logging.getLogger(__name__)


def rental_home(request):
    return render(request, "rentalcars/rentalcar.html")


def rental_list(request, seat_capacity):
    cars = RentalCar.objects.filter(seat_capacity=seat_capacity)
    return render(request, "rentalcars/rental_list.html", {
        "cars": cars,
        "seat_capacity": seat_capacity
    })


def rental_detail(request, car_id):
    car = get_object_or_404(RentalCar, id=car_id)
    return render(request, "rentalcars/rental_details.html", {"car": car})


def rent_now(request, car_id):
    car = get_object_or_404(RentalCar, id=car_id)
    return render(request, "rentalcars/rent_now.html", {"car": car})


def calculate_rent(request, car_id):
    car = get_object_or_404(RentalCar, id=car_id)

    if request.method == 'POST':
        days = int(request.POST.get('days', 1))
        expected_km = request.POST.get('expected_km')
        expected_km = int(expected_km) if expected_km else None

        result = estimate_rent(car, days, expected_km)

        context = {
            "car": car,
            "days": result['days'],
            "expected_km": result['expected_km'],
            "rate_per_km": result['rate_per_km'],
            "total_rent": result['total_rent'],
            "calculated": True,
        }
        return render(request, "rentalcars/rent_result.html", context)

    return render(request, "rentalcars/rent_result.html", {"car": car})


def final_rent_price(request, car_id):
    car = get_object_or_404(RentalCar, id=car_id)
    user_email = None
    if request.user.is_authenticated:
        user_email = request.user.email

    if request.method == 'POST':
        days = int(request.POST.get('days', 1))
        current_km = int(request.POST.get('exp_km', 0))

        result = calculate_final_rent(car, days, current_km)

        # Send billing email
        send_rental_bill_email(user_email, car.car_name, current_km, result['final_price'])
        logger.info(f"Rental bill email sent for {car.car_name} to {user_email}")

        context = {
            "car": car,
            **result,
            "user_email": user_email,
        }
        return render(request, "rentalcars/final_price_checkout.html", context)

    return render(request, "rentalcars/final_price_checkout.html", {"car": car, "user_email": user_email})
