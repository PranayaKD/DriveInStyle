"""
Rental car pricing service — single source of truth for all rate calculations.
"""

# Rate per km based on fuel type and seat capacity
RATES_PER_KM = {
    'petrol': {5: 11, 7: 16},
    'diesel': {5: 9, 7: 14},
}
DEFAULT_RATE_PER_KM = 10

# Fuel cost per litre
FUEL_PRICES = {
    'petrol': 102,
    'diesel': 96,
}
DEFAULT_FUEL_PRICE = 100

# Minimum km per rental day
MIN_KM_PER_DAY = 300

# Extra km surcharge thresholds
EXTRA_KM_SURCHARGE_LOW = 0.02   # < 500 extra km
EXTRA_KM_SURCHARGE_HIGH = 0.04  # >= 500 extra km
EXTRA_KM_THRESHOLD = 500


def get_rate_per_km(fuel_type, seat_capacity):
    """
    Get the rental rate per km based on fuel type and seat capacity.
    
    Args:
        fuel_type (str): Fuel type of the car
        seat_capacity (int): Number of seats (5 or 7)
    
    Returns:
        int: Rate per km in INR
    """
    fuel = (fuel_type or '').strip().lower()
    rates = RATES_PER_KM.get(fuel, {})
    return rates.get(seat_capacity, DEFAULT_RATE_PER_KM)


def get_fuel_rate(fuel_type):
    """
    Get the fuel price per litre for a given fuel type.
    
    Args:
        fuel_type (str): Fuel type of the car
    
    Returns:
        int: Fuel price per litre in INR
    """
    fuel = (fuel_type or '').strip().lower()
    return FUEL_PRICES.get(fuel, DEFAULT_FUEL_PRICE)


def estimate_rent(car, days, expected_km=None):
    """
    Estimate rental cost before the trip.
    
    Args:
        car: RentalCar instance
        days (int): Number of rental days
        expected_km (int, optional): Expected kilometers to drive
    
    Returns:
        dict: Estimation details including rate, total_km, total_rent
    """
    min_km = days * MIN_KM_PER_DAY
    total_km = max(expected_km or 0, min_km)
    rate = get_rate_per_km(car.fuel_type, car.seat_capacity)
    total_rent = total_km * rate

    return {
        'days': days,
        'expected_km': total_km,
        'rate_per_km': rate,
        'total_rent': total_rent,
    }


def calculate_final_rent(car, days, current_km):
    """
    Calculate final rental price after the trip.
    
    Args:
        car: RentalCar instance
        days (int): Number of rental days
        current_km (int): Current odometer reading
    
    Returns:
        dict: Final pricing breakdown
    """
    total_km_driven = car.total_km_driven or 0
    km_diff = current_km - total_km_driven
    min_km = days * MIN_KM_PER_DAY
    chargeable_km = max(km_diff, min_km)

    rate = get_rate_per_km(car.fuel_type, car.seat_capacity)
    base_price = chargeable_km * rate

    # Extra km surcharge
    allowed_km = days * MIN_KM_PER_DAY
    extra_km = km_diff - allowed_km
    surcharge_rate = EXTRA_KM_SURCHARGE_HIGH if extra_km >= EXTRA_KM_THRESHOLD else EXTRA_KM_SURCHARGE_LOW
    accumulated_price = base_price + (base_price * surcharge_rate)

    # Fuel cost (informational — paid by user)
    mileage = car.mileage or 15
    fuel_rate = get_fuel_rate(car.fuel_type)
    fuel_price = (km_diff / mileage) * fuel_rate if mileage else 0

    return {
        'days': days,
        'total_km': km_diff,
        'rate_per_km': rate,
        'accumulated_price': round(accumulated_price, 2),
        'fuel_price': round(fuel_price, 2),
        'final_price': round(accumulated_price, 2),
    }
