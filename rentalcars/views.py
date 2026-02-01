from django.shortcuts import render, get_object_or_404
from .models import RentalCar
from btmapp.utils import send_email_view

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

def rent_now(request,car_id):
    car = get_object_or_404(RentalCar,id =car_id)
    return render(request,"rentalcars/rent_now.html",{"car": car})

def calculate_rent(request, car_id):
    car = get_object_or_404(RentalCar, id=car_id)

    if request.method == 'POST':
        days = int(request.POST.get('days'))
        expected_km = request.POST.get('expected_km')
        min_km = days * 300  

        if expected_km:
            total_km = int(expected_km)
            if total_km < min_km:
                total_km = min_km
        else:
            total_km = min_km

        fuel_type = (car.fuel_type or '').strip().lower()

        if fuel_type == 'petrol':
            if car.seat_capacity == 5:
                rate = 11
            elif car.seat_capacity == 7:
                rate = 16
            else:
                rate = 16
        elif fuel_type == 'diesel':
            if car.seat_capacity == 5:
                rate = 9
            elif car.seat_capacity == 7:
                rate = 14
            else:
                rate = 14
        else:
            rate = 10  

        total_rent = total_km * rate

        context = {
            "car": car,
            "days": days,
            "except_km": total_km,
            "km": rate,
            "fp": total_rent,
            "ca": True,
        }
        return render(request, "rentalcars/rent_result.html", context)
def final_rent_price(request, car_id):
    car = get_object_or_404(RentalCar, id=car_id)
    user_email = None
    if request.user.is_authenticated:
        user_email = request.user.email
    if request.method == 'POST':
        days = int(request.POST.get('days', 1))
        km_now = int(request.POST.get('exp_km', 0))
        total_km_driven = car.total_km_driven or 0
        fuel_type = (car.fuel_type or '').strip().lower()
        if fuel_type == 'petrol':
            if car.seat_capacity == 5:
                price_per_km = 11
            elif car.seat_capacity == 7:
                price_per_km = 16
            else:
                price_per_km = 16
        elif fuel_type == 'diesel':
            if car.seat_capacity == 5:
                price_per_km = 9
            elif car.seat_capacity == 7:
                price_per_km = 14
            else:
                price_per_km = 14
        else:
            price_per_km = 10

        km_diff = km_now - total_km_driven
        
        # Enforce minimum rental distance (300km per day) consistent with estimation
        min_km = days * 300
        chargeable_km = max(km_diff, min_km)
        
        accumulated_price = chargeable_km * price_per_km

        allowed_km = days * 300
        extra_km = km_diff - allowed_km

        if extra_km < 500:
            accumulated_price += accumulated_price * 0.02
        else:
            accumulated_price += accumulated_price * 0.04

        milage = getattr(car, 'milage', 15) 
        fuel_type = (car.fuel_type or '').strip().lower()
        if fuel_type == 'petrol':
            fuel_rate = 102
        elif fuel_type == 'diesel':
            fuel_rate = 96
        else:
            fuel_rate = 100

        fuel_price = (km_diff / milage) * fuel_rate if milage else 0

        # Final price is the accumulated rental cost (fuel is paid by user)
        final_price = accumulated_price
        
        send_email_view(user_email, car.car_name, km_now, final_price)
        print("Email sent")
        

        context = {
            "car": car,
            "days": days,
            "total_km": km_diff,
            "rate": price_per_km,
            "accumulated_price": accumulated_price,
            "fuel_price": fuel_price,
            "final_price": final_price, 
            "user_email": user_email,
        
        }
        
        return render(request, "rentalcars/final_price_checkout.html", context)

    return render(request, "rentalcars/final_price_checkout.html", {"car": car, "user_email": user_email})


