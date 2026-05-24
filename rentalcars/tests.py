# rentalcars/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import RentalCar
from .services import get_rate_per_km, get_fuel_rate, estimate_rent, calculate_final_rent


class PricingServiceTest(TestCase):
    """Tests for the rental pricing service."""

    def test_petrol_5_seater_rate(self):
        """Petrol 5-seater should have rate of 11."""
        self.assertEqual(get_rate_per_km('Petrol', 5), 11)

    def test_petrol_7_seater_rate(self):
        """Petrol 7-seater should have rate of 16."""
        self.assertEqual(get_rate_per_km('Petrol', 7), 16)

    def test_diesel_5_seater_rate(self):
        """Diesel 5-seater should have rate of 9."""
        self.assertEqual(get_rate_per_km('Diesel', 5), 9)

    def test_diesel_7_seater_rate(self):
        """Diesel 7-seater should have rate of 14."""
        self.assertEqual(get_rate_per_km('Diesel', 7), 14)

    def test_default_rate(self):
        """Unknown fuel types should return default rate of 10."""
        self.assertEqual(get_rate_per_km('CNG', 5), 10)
        self.assertEqual(get_rate_per_km('EV', 7), 10)

    def test_case_insensitive_fuel_type(self):
        """Fuel type matching should be case-insensitive."""
        self.assertEqual(get_rate_per_km('PETROL', 5), 11)
        self.assertEqual(get_rate_per_km('diesel', 7), 14)

    def test_petrol_fuel_rate(self):
        """Petrol fuel rate should be 102."""
        self.assertEqual(get_fuel_rate('Petrol'), 102)

    def test_diesel_fuel_rate(self):
        """Diesel fuel rate should be 96."""
        self.assertEqual(get_fuel_rate('Diesel'), 96)

    def test_default_fuel_rate(self):
        """Unknown fuel types should return default rate 100."""
        self.assertEqual(get_fuel_rate('CNG'), 100)


class RentEstimationTest(TestCase):
    """Tests for the rent estimation function."""

    def setUp(self):
        self.car = RentalCar.objects.create(
            car_name='Swift',
            company='Maruti',
            color='Blue',
            fuel_type='Petrol',
            mileage=22,
            seat_capacity=5,
            transmission_type='Manual',
            total_km_driven=50000,
            amenities='AC, Power Steering',
            bootspace='268L',
            rating='4/5',
            car_img='carimg/swift.jpg'
        )

    def test_estimation_minimum_km(self):
        """Estimation should enforce minimum km (300/day)."""
        result = estimate_rent(self.car, days=2, expected_km=100)
        self.assertEqual(result['expected_km'], 600)  # 2 * 300

    def test_estimation_above_minimum(self):
        """Expected km above minimum should be used as-is."""
        result = estimate_rent(self.car, days=1, expected_km=500)
        self.assertEqual(result['expected_km'], 500)

    def test_estimation_total_rent(self):
        """Total rent should be km * rate."""
        result = estimate_rent(self.car, days=1, expected_km=300)
        self.assertEqual(result['total_rent'], 300 * 11)  # petrol 5-seater: 11/km

    def test_estimation_no_expected_km(self):
        """No expected km should fall back to minimum."""
        result = estimate_rent(self.car, days=3)
        self.assertEqual(result['expected_km'], 900)


class FinalRentCalculationTest(TestCase):
    """Tests for the final rent calculation."""

    def setUp(self):
        self.car = RentalCar.objects.create(
            car_name='Innova',
            company='Toyota',
            color='White',
            fuel_type='Diesel',
            mileage=15,
            seat_capacity=7,
            transmission_type='Manual',
            total_km_driven=30000,
            amenities='AC, Music System',
            bootspace='300L',
            rating='5/5',
            car_img='carimg/innova.jpg'
        )

    def test_final_rent_basic(self):
        """Final rent should calculate correctly."""
        result = calculate_final_rent(self.car, days=1, current_km=30300)
        self.assertEqual(result['total_km'], 300)
        self.assertEqual(result['rate_per_km'], 14)  # diesel 7-seater
        self.assertGreater(result['final_price'], 0)

    def test_final_rent_returns_fuel_price(self):
        """Result should include fuel price estimation."""
        result = calculate_final_rent(self.car, days=1, current_km=30300)
        self.assertIn('fuel_price', result)
        self.assertGreater(result['fuel_price'], 0)


class RentalViewTest(TestCase):
    """Tests for rental views."""

    def setUp(self):
        self.client = Client()
        self.car = RentalCar.objects.create(
            car_name='Alto',
            company='Maruti',
            color='Red',
            fuel_type='Petrol',
            mileage=22,
            seat_capacity=5,
            transmission_type='Manual',
            total_km_driven=20000,
            amenities='AC',
            bootspace='177L',
            rating='3/5',
            car_img='carimg/alto.jpg'
        )

    def test_rental_home_loads(self):
        """Rental home page should load."""
        response = self.client.get(reverse('rental_home'))
        self.assertEqual(response.status_code, 200)

    def test_rental_list_loads(self):
        """Rental list should load for a given seat capacity."""
        response = self.client.get(reverse('rental_list', args=[5]))
        self.assertEqual(response.status_code, 200)

    def test_rental_detail_loads(self):
        """Rental detail page should load."""
        response = self.client.get(reverse('rental_details', args=[self.car.id]))
        self.assertEqual(response.status_code, 200)
